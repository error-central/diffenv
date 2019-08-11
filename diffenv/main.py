import subprocess
import sys
import os
from os.path import join, isfile
import requests
import re
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.scalarstring import LiteralScalarString
import pathlib
import json
import git
import string

yaml = YAML()

# Get absolute path of current git repo, if we're in one.
try:
    git_repo = git.Repo('.', search_parent_directories=True)
    git_toplevel = git_repo.git.rev_parse("--show-toplevel")
except:
    # TODO: why cant' we catch `git.exc.InvalidGitRepositoryError` ?
    git_toplevel = None


def run_facet(path):
    """ Run a facet and return the results as a Python object """
    if not os.access(path, os.X_OK):
        sys.stderr.write("ERROR: Facet is not executable: %s" % path)
        return "WARNING: Skipping non-executable facet: %s" % path
    try:
        process = subprocess.Popen(
            [path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        out_decoded = out.decode("utf-8").strip()
        if err:
            combined = out_decoded + err.decode("utf-8")
        else:
            combined = out_decoded

        if not out_decoded:
            # If no stdout, then just return stderr
            return LiteralScalarString(combined)

        try:
            # Try to parse JSON
            return json.loads(out_decoded)
            # NOTE: We're throwing away stderr if present
        except ValueError as e:
            try:
                # If that fails, try to parse YAML
                return yaml.load(out_decoded)
                # NOTE: We're throwing away stderr if present
            except ScannerError as e:
                # If that fails, return raw output
                return LiteralScalarString(out_decoded)

    except subprocess.CalledProcessError as e:
        return LiteralScalarString("ERROR: Problem running %s: %e" % (path, e))


def yaml_format_item(structure, key, depth):
    """
    Attach bars and blank lines
    """
    structure.yaml_set_comment_before_after_key(
        key, '\n', indent=depth * 2)


def extract_facet_dir(dirpath, structure, depth=0):
    """
    Extract facets in folder, recursively building a nested map.
    dirpath: directory to find facets in
    structure: exiting structure of facets that we will add to

    returns: CommentedMap -- a formated yaml nested dictionary
    """
    p = pathlib.Path(dirpath)
    if p.exists():
        for item in sorted(p.iterdir()):
            if str(item).startswith('.'):
                # Ignore hidden files
                continue
            if item.is_dir():
                structure[item.name] = extract_facet_dir(
                    item,
                    structure.get(item.name, CommentedMap()),
                    depth + 1)
            elif item.name not in structure:
                structure[item.name] = str(item.absolute())

            yaml_format_item(structure, item.name, depth)
    return structure


def get_all_facets():
    """
    Collects paths to all facets in current system.
    They are accumulated in `facet_map`
    Returns a formatted facet map of type CommentedMap
    """

    # User facets
    user_facet_dir = os.path.expanduser('~/.diffenv/facets')
    facet_map = extract_facet_dir(user_facet_dir, CommentedMap())

    # Repo facets (if in git repo)
    if git_toplevel is not None:
        git_facet_dir = join(git_toplevel, '.diffenv/facets')
        facet_map = extract_facet_dir(git_facet_dir, facet_map)

    # Default facets
    default_facet_dir = join(os.path.split(
        os.path.abspath(__file__))[0], '..', 'facets')  # dir in our package
    facet_map = extract_facet_dir(default_facet_dir, facet_map)

    return facet_map


def load_config_file(path: str):
    """
    Load a config file formatted in YAML
    """
    with open(path) as f:
        return yaml.load(f)


def collect_env(facets, whitelist):
    """
    Recursively collect environment info from facets specified in config files
    facets: Either a nested map from extract_facet_dir or a node in it, or a leaf (string containing path of facet)
    whitelist: output from parsing a config file, detailing which facets to run
    returns: a formated nested dictionary containing facet output
    """
    if isinstance(facets, str):
        # Actually run the facet and return the results
        return run_facet(facets)
    elif whitelist is None or isinstance(whitelist, str):
        for subdir in list(facets.keys()):
            facets[subdir] = collect_env(facets[subdir], whitelist)
        return facets
    else:
        for subdir in whitelist:
            facets[subdir] = collect_env(facets[subdir], whitelist[subdir])
        subdirs = [s for s in facets]
        for subdir in subdirs:
            if subdir not in whitelist:
                del facets[subdir]
        return facets


def read_file_or_url(name: str):
    """
    Read a filename or a URL and return contents
    """
    if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', name):
        # It's a URL!
        sys.stderr.write("\033[K")
        sys.stderr.write("Downloading " + name + "\r")
        r = requests.get(name)
        sys.stderr.write("\033[K")
        if r.status_code == 404:
            raise Exception(
                name + ' yielded 404 status code. Your upload may have expired.')
        else:
            # Filter out non-printable characters (They break the diff)
            file_text = ''.join(
                filter(lambda x: x in string.printable, r.text))
            return yaml.load(file_text)
    else:
        with open(name) as file:
            return yaml.load(file)

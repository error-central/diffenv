import subprocess
import sys
import os
from os.path import join
import requests
import re
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.scalarstring import LiteralScalarString
import pathlib

yaml = YAML()


def run_facet(name, path):
    """ Run a facet and return the results as a Python object """
    if not os.access(path, os.X_OK):
        sys.stderr.write("ERROR: Facet is not executable: %s" % path)
        return "ERROR: Facet is not executable: %s" % path
    try:
        process = subprocess.Popen([path], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.stderr.write(err)
        result = (out.decode("utf-8"))
        try:
            result = yaml.load(result)
        except ScannerError as e:
            result = LiteralScalarString(result.strip())
        return result

    except subprocess.CalledProcessError as e:
        sys.stderr.write("Problem running %s: %e" % (path, e))
        result += "ERROR: Problem running %s: %e" % (path, e)


def git_toplevel():
    """
    Return absolute path of current git repo, if we're in one.
    Otherwise return None
    """
    try:
        process = subprocess.Popen(
            ['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.stderr.write(err)
        return (out.decode("utf-8").strip())
    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            "Problem running git rev-parse --show-toplevel: %e" % e)
        return None


def yaml_format_item(structure, key, depth):
    """
    Attach bars and blank lines
    """
    structure.yaml_set_comment_before_after_key(
        key, ('=' * (60 - depth * 2)), indent=depth * 2)


def run_facet_dir(dirpath, structure=CommentedMap(), depth=0):
    """
    Execute facets in folder, recursively building a nested map.
    """
    p = pathlib.Path(dirpath)
    if p.exists():
        for item in p.iterdir():
            if item.is_dir():
                structure[item.name] = run_facet_dir(
                    item,
                    structure.get(item.name, CommentedMap()),
                    depth + 1)
            elif item.name not in structure:
                structure[item.name] = run_facet(
                    item.name, str(item.absolute()))

            yaml_format_item(structure, item.name, depth)
    return structure


def collect_env():
            # Default facets
    default_facet_dir = join(os.path.split(
        os.path.abspath(__file__))[0], '..', 'facets')  # dir in our package

    # User facets
    user_facet_dir = os.path.expanduser('~/.diffenv/facets')

    # Repo facets
    git_facet_dir = join(git_toplevel(), '.diffenv/facets')

    # Run the facets!
    yaml_map = run_facet_dir(default_facet_dir,
                             run_facet_dir(user_facet_dir,
                                           run_facet_dir(git_facet_dir)))
    return yaml_map


def read_file_or_url(name):
    if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', name):
        # it's a URL!
        r = requests.get(name)
        if r.status_code == 404:
            raise Exception(
                name + ' yielded 404 status code. Your upload may have expired.')
        else:
            return yaml.load(r.text)
    else:
        with open(name) as file:
            return yaml.load(file)

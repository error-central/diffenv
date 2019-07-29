import subprocess
import sys
import os
from os import listdir
from os.path import isfile, join
import sys
import requests
import re
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.comments import CommentedMap
from io import StringIO

yaml = YAML()

def run_facet(name, path):
  """ Run a facet and return the results as a Python object"""
  if not os.access(path, os.X_OK):
    sys.stderr.write("ERROR: Facet is not executable: %s" % path)
    return (result + "ERROR: Facet is not executable: %s" % path)
  try:
    process = subprocess.Popen([path], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
      sys.stderr.write(err)
    result = (out.decode("utf-8"))
    try:
      result = yaml.load(result)
    except ScannerError as e:
      # does not seem to be valid yaml (or JSON)
      pass
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
        ['git','rev-parse','--show-toplevel'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
      sys.stderr.write(err)
    return (out.decode("utf-8").strip())
  except subprocess.CalledProcessError as e:
    sys.stderr.write(
        "Problem running git rev-parse --show-toplevel: %e" % e)
    return None

def collect_env():
  # Default facets
  default_facet_dir = join(os.path.split(
      os.path.abspath(__file__))[0], '..', 'facets') # dir in our package
  default_facets = [(default_facet_dir, f) for f in listdir(
    default_facet_dir) if isfile(join(default_facet_dir, f))]
  default_facets.sort()
  # User facets
  user_facet_dir = os.path.expanduser('~/.diffenv/facets')
  user_facets = [(user_facet_dir, f) for f in listdir(user_facet_dir) if isfile(
    join(user_facet_dir, f))] if os.path.isdir(user_facet_dir) else []
  user_facets.sort()
  # Repo facets
  git_facet_dir = join(git_toplevel(), '.diffenv/facets')
  git_facets = [(git_facet_dir, f) for f in listdir(git_facet_dir) if isfile(
    join(git_facet_dir, f))] if os.path.isdir(git_facet_dir) else []
  git_facets.sort()
  # Sort all facets
  facets = git_facets + user_facets + default_facets

  # Run the facets!
  yaml_map = CommentedMap([(facet_name,
                            run_facet(facet_name, join(facet_dir, facet_name)))
                           for (facet_dir, facet_name) in facets])

  # format the facet output
  for _, facet_name in facets:
    yaml_map.yaml_set_comment_before_after_key(facet_name, ('=' * 60))
  buf = StringIO()
  yaml.dump(yaml_map, buf)
  return buf.getvalue()


def read_file_or_url(name):
  if re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', name):
    # it's a URL!
    r = requests.get(name)
    if r.status_code == 404:
      raise Exception(name + ' yielded 404 status code. Your upload may have expired.')
    else:
      return [l + '\n' for l in r.text.splitlines()]
  else:
    with open(name) as file:
      return file.readlines()

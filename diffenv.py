#!/usr/bin/env python3

import subprocess
import sys
import os
from os import listdir
from os.path import isfile, join
import argparse

import diffviewer

# Handle arguments

parser = argparse.ArgumentParser(description='Diff total development environment.')
parser.add_argument('-o', '--output', help='output to file instead of stdout')
parser.add_argument('-c', '--compare', nargs='*', default=None, help='display diff between two environments')
args = parser.parse_args()

def run_facet(name, path):
  """ Run a facet and return the results as string """
  result = ''
  result += '\n' + ('=' * 70) + '\n'
  result += name
  result += '\n' + ('=' * 70) + '\n'
  if not os.access(path, os.X_OK):
    return (result + "ERROR: Facet is not executable: %s" % path)
  try:
    process = subprocess.Popen([path], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
      sys.stderr.write(err)
    result += (out.decode("utf-8"))
  except subprocess.CalledProcessError as e:
    sys.stderr.write("Problem running %s: %e" % (path, e))
    result += "ERROR: Problem running %s: %e" % (path, e)
  return result


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
  default_facet_dir = './facets'
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
  facets = default_facets + user_facets + git_facets

  # Run the facets!
  diffenv = ''
  for (facet_dir, facet_name) in facets:
    diffenv += run_facet(facet_name, join(facet_dir, facet_name))
  return diffenv


# Handle outputting to file or stdout
outfilestream = sys.stdout if args.output is None else open(args.output, 'w')

if args.compare is None:
  # Output our results
  print(collect_env(), file=outfilestream)
else:
  if len(args.compare) == 0:
    # TODO compare to current state to most recent commit
    print("Git hook integration not implemented yet")
  else:
    files = []
    with open(args.compare[0]) as other_file:
      files.append(other_file.readlines())
    if len(args.compare) == 1:
      files = [[l + '\n' for l in collect_env().splitlines()]] + files
    else:
      with open(args.compare[1]) as other_file:
        files.append(other_file.readlines())

    diffviewer.display_diff(files[0],
                            files[1],
                            outfilestream)

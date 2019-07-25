#!/usr/bin/env python3

import subprocess
import sys
import os
from os import listdir
from os.path import isfile, join
import argparse

parser = argparse.ArgumentParser(description='Diff total development environment.')
parser.add_argument('-o', '--output', help='output to file instead of stdout')
args = parser.parse_args()

def run_facet(name, path):
  """ Run a facet and return the results as string """
  result = ''
  result += '\n' + ('=' * 70) + '\n'
  result += name
  result += '\n' + ('=' * 70) + '\n'
  try:
    process = subprocess.Popen([path], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
      sys.stderr.write(err)
    result += (out.decode("utf-8"))
  except subprocess.CalledProcessError as e:
    sys.stderr.write("Problem running %s: %e" % (path, e))
    result += "Problem running %s: %e" % (path, e)
  return result

# Default facets
default_facet_dir = './facets'
default_facets = [(default_facet_dir, f) for f in listdir(
    default_facet_dir) if isfile(join(default_facet_dir, f))]
# User facets
user_facet_dir = os.path.expanduser('~/.diffenv/facets')
user_facets = [(user_facet_dir, f) for f in listdir(user_facet_dir) if isfile(
    join(user_facet_dir, f))] if os.path.isdir(user_facet_dir) else []
# Sort all facets
facets = default_facets + user_facets
facets.sort()  # Sort them alphabetically
# Run the facets!
diffenv = ''
for (facet_dir, facet_name) in facets:
  diffenv += run_facet(facet_name, join(facet_dir, facet_name))
# Handle outputting to file or stdout
outfilestream = sys.stdout if args.output is None else open(args.output, 'w')
# Output our results
print(diffenv, file=outfilestream)


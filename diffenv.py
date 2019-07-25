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
  result += script
  result += '\n' + ('=' * 70) + '\n'
  try:
    process = subprocess.Popen([path], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
      sys.stderr.write(err)
    result += (out.decode("utf-8"))
  except subprocess.CalledProcessError as e:
    sys.stderr.write("Problem running %s: %e" % (script, e))
    result += "Problem running %s: %e" % (script, e)
  return result

facet_path = './facets'

facetScripts = [f for f in listdir(facet_path) if isfile(join(facet_path, f))]
facetScripts.sort() # Sort them alphabetically

diffenv = ''
for script in facetScripts:
  diffenv += run_facet(script, join(facet_path, script))

# Handle outputting to file or stdout
outfilestream = sys.stdout if args.output is None else open(args.output, 'w')

print(diffenv, file=outfilestream)


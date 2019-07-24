import subprocess
import sys
import os
from os import listdir
from os.path import isfile, join

mypath = './facets'

facetScripts = [f for f in listdir(mypath) if isfile(join(mypath, f))]
facetScripts.sort()

diffenv = ''
for script in facetScripts:
  diffenv += '\n' + ('=' * 70) + '\n'
  diffenv += script
  diffenv += '\n' + ('=' * 70) + '\n'
  try:
      process = subprocess.Popen(
          [join(mypath, script)], stdout=subprocess.PIPE)
      out, err = process.communicate()
      if err:
        sys.stderr.write(err)
      # TODO: Check if err happened. None or empty string?
      diffenv += out.decode("utf-8")
  except subprocess.CalledProcessError as e:
      sys.stderr.write("Problem running %s" % script)

print(diffenv)


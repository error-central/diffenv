import argparse
import subprocess
import os
from os import listdir
from os.path import isfile, join

mypath = './facets'

facetScripts = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for script in facetScripts:
  print(script)
  try:
      subprocess.run(
          [join(mypath, script)], check=True)
  except subprocess.CalledProcessError as e:
      print("Problem running %s" % script)





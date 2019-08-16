[![Build Status](https://travis-ci.com/error-central/diffenv.svg?branch=master)](https://travis-ci.com/error-central/diffenv)

# diffenv

##  Overview

diffenv gathers and compares development environments. It defines 
a simple standard for storing a complete picture of an environment
as a structured collection of "facets" such as "python", "shell",
"git", etc.

![output](https://user-images.githubusercontent.com/673455/62836101-182d1200-bc60-11e9-95c7-1f52dfb197b7.gif)


### Output your current environment
```yaml
#$ diffenv
python:
  python-version: Python 3.7.3
shell:
  envvars:
    EDITOR: sublw
    GIT_EDITOR: subl -w
    API_ENDPOINT: http://api.lvh.me:4000
    PRISMA_ENDPOINT: http://prisma:4466
os:
  timezone: 0200
  version: Darwin 18.7.0 x86_64

# ...trimmed 
```
(Simplified example. See [full example](https://raw.githubusercontent.com/error-central/diffenv/master/examples/gabe_env.yaml) here)

### Share your environment with co-worker
```
#$ diffenv --share

Your env was uploaded to: https://transfer.sh/P1gQZ/env.yaml

Run the following line on comparison environment:

diffenv --compare https://transfer.sh/P1gQZ/env.yaml
```

### Diff your environment with co-worker
```diff
#$ diffenv --compare https://transfer.sh/P1gQZ/env.yaml
git:
  git-user-name:
-    <<-: Stan James
+    +>>: Gabriel Pickard
  version:
-    <<-: git version 2.22.0
+    +>>: git version 2.11.0
os:
  version:
-    <<-: Darwin 18.7.0 x86_64
+    +>>: Linux 4.19.34-04457-g5b63d4390e96 x86_64
python:
  python-version:
-    <<-: Python 3.7.3
+    +>>: Python 2.7.13
  python3-version:
-    <<-: Python 3.7.3
+    +>>: Python 3.5.3
  which-python:
-    <<-: /usr/local/opt/python/libexec/bin/python
+    +>>: /usr/bin/python

# ...trimmed 
```

### Include environment in submitted issues

```bash
#$ diffenv --issue

# Browser will open with new issue
```

<img width="407" alt="Screen Shot 2019-08-14 at 6 43 06 PM" src="https://user-images.githubusercontent.com/673455/63039406-7f96cc00-bec3-11e9-88e8-cb49bc931140.png">


### Compare with past commits

```diff
#$ diffenv --compare .diffenv/commits/2b19c9e47af0828c8775ee231768631e0b06ae0f.diffenv
git:
  version:
-    <<-: git version 2.11.0
+    +>>: git version 2.22.0
python:
  python-version:
-    <<-: Python 3.7
+    +>>: Python 3.7.3
```

Note this requires the git commit hooks to have been installed, so that diffenv is run on each commit.
```
#$ diffenv --add-hooks
```


## Installation

```bash
python3 -m pip install diffenv
```
Currently diffenv only supports Python 3.

## Use

To output your current development environment to stderr:
```
diffenv
```

To compare your environment with @werg:
```bash
diffenv -c https://raw.githubusercontent.com/error-central/diffenv/master/examples/gabe_env.yaml
```

To share your environment with a coworker for comparison:
```bash
diffenv --share
```

For a complete list of command line options run:
```bash
$ diffenv --help

usage: diffenv [-h] [-o OUTPUT] [-c COMPARE] [--add-hooks] [--share] [--issue]
               [--post POST] [--config CONFIG] [--ignore-config] [--no-color]
               [--no-paging] [--version]

Diff your total environment. Run without any params to simply output current
environment state as YAML.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output to file instead of stdout
  -c COMPARE, --compare COMPARE
                        file or URL to compare against the current env
  --add-hooks           install git hooks in current repo and exit
  --share               store current env and return URL that can be shared
  --issue               create github issue
  --post POST           POST env to specific URL when sharing; must be used
                        with --share
  --config CONFIG       load config from specific file
  --ignore-config       ignore configs and run all facets
  --no-color            don't color diff output
  --no-paging           don't use less for paging output
  --version             display version and exit
```

## Customization

diffenv can be customized for a user or for a repo.  Customizations are put in a directory named `.diffenv` in the user's home directory or the git repos top directory.

### Custom Facets

Custom facets for a git repo should be saved in `.diffenv/facets/<yourfacet>`

The facet file itself needs to be excutable (`chmod +x <yourfacet>`).

### Configuration

You can limit which facets are run with a yaml file saved in `.diffenv/config.yaml`

See `example_config.yaml` for more information.

## Contributing to diffenv

### Development install

If you are developing locally, do _not_ install as above, and instead run the following in the repo root directory:

```bash
# Remove global installation of diffenv, if present
pip3 uninstall diffenv

# depending on your setup you may have to prefix sudo to this command
pip3 install --editable .
```

Now `diffenv` will always point to your local repo, including any changes.


### Testing

```bash
python3 -m unittest tests/tests.py
```

For testing on docker containers:
```bash
docker pull python
docker run -it python bash
# Now e.g. `pip install diffenv`
```

### Creating a release

First edit `setup.py` and bump the version, then:

```bash
python3 setup.py sdist
# modify the below to match the file of the version you just created
twine upload dist/diffenv-
```

[![Build Status](https://travis-ci.com/error-central/diffenv.svg?branch=master)](https://travis-ci.com/error-central/diffenv)

# diffenv

##  Overview

diffenv gathers and compares runtime environments. It defines a simple standard for storing a complete picture of a development environment.

![output](https://user-images.githubusercontent.com/673455/62836101-182d1200-bc60-11e9-95c7-1f52dfb197b7.gif)


### Save your current environment
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


### Use cases
* Add environment data to bug reports, even automatically. [Example](https://github.com/error-central/diffenv/issues/29)
* Diagnose what subtle difference in environment is making things fail on your coworker's machine.
* Compare your current environment against past commits when things worked.

## Options

```
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
diffenv --help
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
# depending on your setup you may have to prefix sudo to this command
pip3 install --editable .
```

Now `diffenv` will always point to your local repo, including any changes.


For testing on docker containers:
```bash
docker pull python
docker run -it python bash
# Now e.g. `pip install diffenv`
```

### Testing

```bash
python3 -m unittest tests/tests.py
```


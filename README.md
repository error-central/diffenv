[![Build Status](https://travis-ci.com/error-central/diffenv.svg?branch=master)](https://travis-ci.com/error-central/diffenv)

# diffenv

##  Overview

diffenv gathers and compares development environments. It defines 
a simple standard for storing a complete picture of an environment
as a structured collection of facets such as "python", "shell",
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
    PRISMA_ENDPOINT: http://prisma:4466
    GOOGLE_API_KEY(HASHED): 603ade004ce4bb13c3f66bc1644164ca(HASH)
os:
  timezone: 0200
  version: Darwin 18.7.0 x86_64

# ...trimmed
```
(Simplified example. See [full example](https://raw.githubusercontent.com/error-central/diffenv/master/examples/gabe_env.yaml) here)

You can also get just specific facets:

```bash
# Get all python-relevant information
diffenv --facet python

# List environment variables
diffenv -f shell:envvars
```

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

If you are an open-source project maintainer you can use diffenv to structure the submission of bug reports. Tell your users to specify the conditions under which their bug occurs by sending along their diffenv output. This way you can get significantly more detailed insight from the get-go without having to go back and forth with the reporter of the bug.

For github issues we provide a handy way to submit a new issue and include a local diffenv dump directly from the command line.

```bash
#$ diffenv --issue

# Browser will open a Github issue with env data automatically added:
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
               [--no-paging] [--version] [-f FACET]

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
  -f FACET, --facet FACET
                        run a specific facet

More information and source code at https://github.com/error-central/diffenv

```

## Customization

diffenv can be customized for a user or for a repo.  Customizations are put in a directory named `.diffenv` in the user's home directory or the git repos top directory.

### Custom Facets

Custom facets for a git repo should be saved in `.diffenv/facets/<yourfacet>`

The facet file itself needs to be excutable (`chmod +x <yourfacet>`).

### Configuration

You can limit which facets are run with a yaml file saved in `.diffenv/config.yaml`

Here's an example config:

```yaml
# Currently there is only one relevant part of the config, facets.
facets:
  # If you give the name of a directory, it will run all facets in it.
  # In this case, we'll run every facet within `python`.
  python:
  
  # ...or you can list all the way down to the facet within a directory.
  # Here we'll only run the `node-version` facet.
  nodejs:
    node-version:
    
  git:
  
  os:
  
  shell:
    # You can also provide command line arguments as list to the facet.
    # In this case we pass the `shell` facet a whitelist of environment 
    # variables to show.
    envvars:
      - DISPLAY
      - USER
      - PATH
      - PWD
      - HOME
      - SHELL
      - COLORTERM
      - TERM
  directory:
    # In this case we restrict how deep we recur into child directories
    listing: 1
```


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

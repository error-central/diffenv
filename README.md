[![Build Status](https://travis-ci.com/error-central/diffenv.svg?branch=master)](https://travis-ci.com/error-central/diffenv)

# diffenv
Output and compare all facets of development environments.

##  Overview

diffenv gathers and compares runtime environment metadata. A standard way of capturing a complete picture of a development environment.

![output](https://user-images.githubusercontent.com/673455/62836101-182d1200-bc60-11e9-95c7-1f52dfb197b7.gif)


### Simplified example
```bash
$ diffenv
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
```

[Full example output](https://raw.githubusercontent.com/error-central/diffenv/master/examples/gabe_env.yaml).

### Use cases
* Add environment data to bug reports in a _standardized format_. [Example](https://github.com/error-central/diffenv/issues/29)
* Diagnose what subtle difference is making things fail on your coworker's machine.
* Compare your current environment against past recorded state when things still worked.

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

### Testing

```
python3 -m unittest tests/tests.py
```


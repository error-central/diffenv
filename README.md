# diffenv
Output and compare all facets of development environments.

##  Overview

diffenv gathers and compares runtime environment metadata, intended to remedy the common developer situation of "But it works on my machine! What's different about your environment?"

Simplified example usage:
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

[Full example output](https://raw.githubusercontent.com/error-central/diffenv/master/examples/stan-diffenv.yaml).


## Installation

### Standard
To install normally:

```bash
pip3 install diffenv
```

### Development

If you are developing locally, do _not_ install as above, and instead run the following in the repo root directory:

```bash
# depending on your setup you may have to prefix sudo to this command
pip install --editable .
```

Now `diffenv` will always point to your local repo, including any changes.


## Use

To output your current development environment to stderr:
```
diffenv
```

To compare your environment with @wanderingstan:
```bash
diffenv -c https://raw.githubusercontent.com/error-central/diffenv/master/examples/stan-diffenv.yaml
```

To share your environment with a coworker for comparison:
```bash
diffenv --share
```
## Customization

diffenv can be customized for a user or for a repo.  Customizations are put in a directory named `.diffenv` in the user's home directory or the git repos top directory.

### Custom Facets

Custom facets for a git repo should be saved in `.diffenv/facets/<yourfacet>`

The facet file itself needs to be excutable (`chmod +x <yourfacet>`).

### Configuration

You can limit which facets are run with a yaml file saved in `.diffenv/config.yaml`

See `example_config.yaml` for more information.

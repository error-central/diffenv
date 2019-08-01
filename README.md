# diffenv
Compare development environments.

## Installation

### Standard
To install normally:

```bash
pip3 install diffenv
# call command with
diffenv
```

### Development

If you are developing locally, do _not_ install as above, and instead run the following in the repo root directory:

```bash
# depending on your setup you may have to prefix sudo to this command
pip install --editable .
```

The above should keep updating with local changes to your repository.

If you ran the above command with `sudo`, you may have to do the following:

```bash
sudo chown -R youruser:youruser diffenv.egg-info dist
```

Now you can run
```bash
diffenv
```

## Customization

diffenv can be customized for a user or for a repo.  Customizations are put in a directory named `.diffenv` in the user's home directory or the git repos top directory.

### Custom Facets

Custom facets for a git repo should be saved in `.diffenv/facets/<yourfacet>`

The facet file itself needs to be excutable (`chmod +x <yourfacet>`).

### Configuration

You can limit which facets are run with a yaml file saved in `.diffenv/config.yaml`

See `example_config.yaml` for more information.

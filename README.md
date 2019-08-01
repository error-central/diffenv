# diffenv
Compare development environments

## Install

To install normally:

```bash
pip3 install diffenv
# call command with
diffenv
```


## Development

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

# diffenv
Compare development environments


## Development

In order to run a development install run:

```console
  # depending on your setup you may have to prefix sudo to this command
  python3 setup.py develop
```

The above should keep updating with local changes to your repository.

If you ran the above command with `sudo`, you may have to do the following:
```console
sudo chown -R youruser:youruser diffenv.egg-info dist
```

Now you can run
```
  diffenv
```

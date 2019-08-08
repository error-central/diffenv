import tempfile
import subprocess
import os

# From:
# https://chase-seibert.github.io/blog/2012/10/31/python-fork-exec-vim-raw-input.html


def raw_input_editor(default=None, editor=None, prefix=None, suffix=None):
    ''' like the built-in raw_input(), except that it uses a visual
    text editor for ease of editing. Unline raw_input() it can also
    take a default value. '''
    with tempfile.NamedTemporaryFile(mode='r+', prefix=prefix, suffix=suffix) as tmpfile:
        if default:
            tmpfile.write(default)
            tmpfile.flush()
        subprocess.check_call([editor or get_editor(), tmpfile.name])
        tmpfile.seek(0)
        return tmpfile.read().strip()


def get_editor():
    return (os.environ.get('VISUAL')
            or os.environ.get('EDITOR')
            or 'vi')

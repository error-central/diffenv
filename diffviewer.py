import difflib
from colorama import Fore, Back, Style, init


def unified_diff(fromlines, tolines):
  diff = difflib.unified_diff(fromlines, tolines, n=99999999, lineterm='')
  for i, line in enumerate(diff):
    if i > 2:
      yield line


def display_diff(fromlines, tolines, outfilestream):
  diff = unified_diff(fromlines, tolines)
  outfilestream.writelines(color_diff(diff))


def color_diff(diff):
  for line in diff:
    if line.startswith('+'):
      yield Fore.GREEN + line + Fore.RESET
    elif line.startswith('-'):
      yield Fore.RED + line + Fore.RESET
    elif line.startswith('^'):
      yield Fore.BLUE + line + Fore.RESET
    else:
      yield line

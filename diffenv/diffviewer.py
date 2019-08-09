import difflib
from colorama import Fore, Back
import collections
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from io import StringIO
from copy import deepcopy
import typing

""" Display differences between two environments. """

yaml = YAML()

A_MARKER = '<<-'
B_MARKER = '+>>'

A_MARKER_TXT = '<--'
B_MARKER_TXT = '++>'


def diff(fromfile, tofile, do_color: bool) -> typing.List[str]:
    """
    Primary funciton. Display diff between two YAML files.
    fromfile: ordereddict (YAML structrue)
    tofile: ordereddict (YAML structrue)
    do_color: Boolean indicating whether to colorize output
    returns: Array of lines
    """
    buf = StringIO()
    yaml.dump(diff_nested(fromfile, tofile), buf)
    difflines = buf.getvalue().splitlines(True)
    if do_color:
        difflines = colorize_diff(difflines)
    return difflines


def string_diff(fromlines: typing.List[str], tolines: typing.List[str]):
    diff = difflib.unified_diff(fromlines, tolines, n=8, lineterm='\n')
    for i, line in enumerate(diff):
        if i > 2:
            if line.startswith('-'):
                yield A_MARKER_TXT + line[1:]
            elif line.startswith('+'):
                yield B_MARKER_TXT + line[1:]
            else:
                yield line


def colorize_diff(diff: typing.List[str]):
    """
    Add terminal colors to a diff
    """
    marking = ''
    col = 0
    for line in diff:
        if A_MARKER in line or A_MARKER_TXT in line:
            marking = Fore.GREEN
        elif B_MARKER in line or B_MARKER_TXT in line:
            marking = Fore.RED
        elif len(line) - len(line.lstrip()) < col:
            # in case of unindent reset marking color
            marking = ''

        # keep track of leading whitespace to catch unindent
        col = len(line) - len(line.lstrip())
        line = marking + line + Fore.RESET
        if A_MARKER_TXT in line or B_MARKER_TXT in line:
            # reset because text lines are marked individually
            marking = ''
        yield line


def diff_nested(m1, m2):
    """
    Recursively computes diff of two nested YAML structures.
    Note m1, m2 may also be strings
    """
    if isinstance(m1, str) or type(m1) != type(m2):
        # We are comparing values (likely strings)directly
        result = CommentedMap([(A_MARKER, m1),
                               (B_MARKER, m2)])

        if isinstance(m1, str) and isinstance(m2, str):
            fromlines = str(m1).splitlines()
            tolines = str(m2).splitlines()
            if min(len(fromlines), len(tolines)) > 5:
                diff = list(string_diff(fromlines, tolines))
                if len(diff) / (len(fromlines) + len(tolines)) < 1.0:
                    # there is material overlap
                    # so show string diff
                    result = LiteralScalarString('\n'.join(diff))
        return result

    elif isinstance(m1, collections.Mapping):
        # We are comparing dictionaries
        result = deepcopy(m1)
        for key in m1:
            if m1[key] == m2.get(key):
                del result[key]
            else:
                result[key] = diff_nested(m1[key], m2.get(key))

        for key in m2:
            if key not in m1:
                result[key] = diff_nested(None, m2[key])
        return result

    elif isinstance(m1, collections.Sequence):
        # We are comparing lists
        result = deepcopy(m1)
        if len(m1) == len(m2):
            to_delete = []
            for i, (item1, item2) in enumerate(zip(m1, m2)):
                if item1 == item2:
                    to_delete.append(i)
                else:
                    print(item1, item2)
                    print(type(item1))
                    result[i] = diff_nested(item1, item2)

            for i in sorted(to_delete, reverse=True):
                del result[i]

            return result

        else:
            # If the lists are unequal size
            # does not handle nested sequences
            matches = difflib.SequenceMatcher(
                None, m1, m2).get_matching_blocks()
            m1 = result
            m2 = deepcopy(m2)
            for i1, i2, size in reversed(matches):
                for i in range(size):
                    del m1[i1]
                    del m2[i2]
            return CommentedMap([(A_MARKER, m1),
                                 (B_MARKER, m2)])
    else:
        # Some other kind of type compared directly
        return CommentedMap([(A_MARKER, m1),
                             (B_MARKER, m2)])

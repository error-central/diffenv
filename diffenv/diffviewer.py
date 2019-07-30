import difflib
from colorama import Fore, Back
import collections
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from io import StringIO
from copy import deepcopy

yaml = YAML()

A_MARKER = '<<-'
B_MARKER = '+>>'

A_MARKER_TXT = '<--'
B_MARKER_TXT = '++>'


def string_diff(fromlines, tolines):
    diff = difflib.unified_diff(fromlines, tolines, n=8, lineterm='\n')
    for i, line in enumerate(diff):
        if i > 2:
            if line.startswith('-'):
                yield A_MARKER_TXT + line[1:]
            elif line.startswith('+'):
                yield B_MARKER_TXT + line[1:]
            else:
                yield line


def display_diff(fromfile, tofile, outfilestream):
    buf = StringIO()
    yaml.dump(diff_nested(fromfile, tofile), buf)
    difflines = buf.getvalue().splitlines(True)
    outfilestream.writelines(color_diff(difflines))


def color_diff(diff):
    marking = False
    col = 0
    for line in diff:
        if not marking and A_MARKER in line:
            if B_MARKER in line:
                # Handle single-line case (if applicable?)
                i = line.index(B_MARKER)
                yield Fore.GREEN + line[:i] + Fore.RESET + Fore.RED + line[i:] + Fore.RESET
            else:
                marking = True
                yield Fore.GREEN + line

        elif marking and B_MARKER in line:
            col = line.index(B_MARKER)
            yield Fore.RESET + Fore.RED + line

        elif marking and len(line) - len(line.lstrip()) < col:
            # deindented
            marking = False
            yield Fore.RESET + line

        elif not marking and A_MARKER_TXT in line:
            yield Fore.GREEN + line + Fore.RESET
        elif not marking and B_MARKER_TXT in line:
            yield Fore.RED + line + Fore.RESET

        else:
            yield line


def diff_nested(m1, m2):
    """ Computes diff of two nested YAML structures. """
    if isinstance(m1, collections.Mapping) and m2:
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

    elif isinstance(m1, collections.Sequence) and not isinstance(m1, str) and m2:
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
        # We are comparing values (likely strings) directly
        result = CommentedMap([(A_MARKER, m1),
                               (B_MARKER, m2)])
        if isinstance(m1, str) and m2:
            fromlines = m1.splitlines()
            tolines = m2.splitlines()
            if min(len(fromlines), len(tolines)) > 5:
                diff = list(string_diff(fromlines, tolines))
                if len(diff) / (len(fromlines) + len(tolines)) < 1.0:
                    # there is material overlap
                    # so show string diff
                    result = LiteralScalarString('\n'.join(diff))

        return result

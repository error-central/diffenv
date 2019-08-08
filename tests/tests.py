import unittest
import subprocess
import sys

# Unit tests for diffenv
#
# To run:
#     python3 -m unittest tests.py


class TestStringMethods(unittest.TestCase):

    def test_non_git(self):
        """ Test running in a non-git repo """
        # TODO
        # self.assertEqual('foo'.upper(), 'FOO')
        pass

    def test_plain(self):
        """ Test running with no params """
        # TODO
        # self.assertEqual('foo'.upper(), 'FOO')
        pass

    def test_sharing(self):
        """ Test sharing env """
        process = subprocess.Popen(
            ['diffenv', '--share'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.stderr.write(err)
        result_lines = (out.decode("utf-8")).split("\n")
        # Get the url

        # Should be e.g. diffenv --compare https://transfer.sh/15xMWL/diff
        diff_command = result_lines[2]
        self.assertEqual(diff_command[:26], "diffenv --compare https://")

        process = subprocess.Popen(
            diff_command.split(" "), stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.stderr.write(err)
        result_lines = out.decode("utf-8")

        # Should show that env is identical
        self.assertEqual(result_lines, "{}\n")

    def test_compare_http(self):
        """ Test comparing with remote env """
        # TODO
        # self.assertEqual('foo'.upper(), 'FOO')
        pass

    def test_compare_file(self):
        """ Test comparing with a file """
        # TODO
        # self.assertEqual('foo'.upper(), 'FOO')
        pass

    def test_passed_config(self):
        """ Test with passing in a cofig file """
        # TODO
        # self.assertEqual('foo'.upper(), 'FOO')
        pass


if __name__ == '__main__':
    unittest.main()

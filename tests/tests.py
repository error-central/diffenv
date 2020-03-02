import unittest
import subprocess
import sys

# Unit tests for diffenv
#
# Run from project root as:
#     python3 -m unittest tests/tests.py


class TestStringMethods(unittest.TestCase):

    # def test_non_git(self):
    #     """ Test running in a non-git repo """
    #     # TODO
    #     # self.assertEqual('foo'.upper(), 'FOO')
    #     pass

    # def test_plain(self):
    #     """ Test running with no params """
    #     # TODO
    #     # self.assertEqual('foo'.upper(), 'FOO')
    #     pass

    def test_readme_for_help(self):
        process = subprocess.Popen(
            ['diffenv', '-h'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.stderr.write(err)
        help_out = (out.decode("utf-8"))

        # print(help_out)

        with open('./README.md', 'r') as readme_file:
            readme = readme_file.read()

        print(readme)

        self.assertIn(help_out, readme)


    def test_sharing(self):
        """ Test sharing env """
        process = subprocess.Popen(
            ['diffenv', '--share'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.stderr.write(err)
        result_lines = (out.decode("utf-8")).split("\n")

        # Get the url
        # 5th line Should be e.g. `diffenv --compare https://transfer.sh/15xMWL/diff`
        diff_command = result_lines[5]
        print(result_lines)
        self.assertEqual(diff_command[:26], "diffenv --compare https://")

        process = subprocess.Popen(
            diff_command.split(" "), stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            sys.stderr.write(err)
        result_lines = out.decode("utf-8")

        # Should show that env is identical
        self.assertEqual(result_lines, "{}\n")

    # def test_compare_http(self):
    #     """ Test comparing with remote env """
    #     # TODO
    #     # self.assertEqual('foo'.upper(), 'FOO')
    #     pass

    # def test_compare_file(self):
    #     """ Test comparing with a file """
    #     # TODO
    #     # self.assertEqual('foo'.upper(), 'FOO')
    #     pass

    # def test_passed_config(self):
    #     """ Test with passing in a cofig file """
    #     # TODO
    #     # self.assertEqual('foo'.upper(), 'FOO')
    #     pass


if __name__ == '__main__':
    unittest.main()

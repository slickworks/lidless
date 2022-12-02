import pprint
from .base import BaseEndToEnd


class TestCmdArgs(BaseEndToEnd):

    def lines_contain(self, lines, contents):
        for line in lines:
            if contents in line:
                return True
        return False

    def assert_output_contains(self, cmd, contents):
        output = self.call(cmd)
        if not self.lines_contain(output, contents):
            lines = pprint.pformat(output)
            raise AssertionError(f"Output does not have expected contents.\n\
                Contents: '{contents}'.\n\
                Output: {lines}"
            )
        return output

    def assert_displays_help(self, cmd):
        output = self.call(cmd)
        if not output[0].startswith("usage:"):
            lines = pprint.pformat(output)
            raise AssertionError(f"Output did not display help: {lines}")
        return output
    
    def test_with_help(self):
        self.assert_displays_help("help")

    def test_no_args(self):
        self.assert_displays_help("")

    def test_invalid_arg(self):
        self.assert_displays_help("foobar")
        self.assert_output_contains("foobar", "invalid choice")

    def test_with_target_cmd_with_missing_target(self):
        self.assert_displays_help("backup")
        self.assert_output_contains("backup", "the following arguments are required: target")

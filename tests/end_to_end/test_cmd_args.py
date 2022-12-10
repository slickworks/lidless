import pprint
from .base import BaseEndToEnd


class TestTopLevelArgs(BaseEndToEnd):
    """
    Tests the top args to make sure we display help and error messages.
    Not exhaustive, just a canary test.
    """

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
        output = self.assert_displays_help("foobar")
        self.assert_output_contains(output, "invalid choice")

    def test_with_target_cmd_with_missing_target(self):
        output = self.assert_displays_help("backup")
        self.assert_output_contains(
            output, "the following arguments are required: target"
        )

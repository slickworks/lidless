from .base import BaseEndToEnd


class TestCmdArgs(BaseEndToEnd):
    def assert_displays_help(self, cmd):
        output = self.call(cmd)
        print(output)
        assert output[0].startswith("usage:")
        return output
    
    def test_with_help(self):
        self.assert_displays_help("help")

    def test_no_args(self):
        self.assert_displays_help("")

    def test_invalid_arg(self):
        output = self.assert_displays_help("foobar")
        assert "invalid choice" in output[1]

    def test_with_target_cmd_with_missing_target(self):
        output = self.assert_displays_help("backup")
        assert "the following arguments are required: target" in output[1]
    

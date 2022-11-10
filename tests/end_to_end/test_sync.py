from .base import EndToEndTest


class TestConfig(EndToEndTest):
    """
    test
        correct remotes are picked up
        paths concatenated correctly
    
    """

    def test_1(self):
        files = """
        foo
        foo/bar.txt
        """
        self.setSrcDir(files)
        self.getConfigSrcDir()
        self.cmd_backup(remote_keys=["test"])
        self.assertDest(files)

        # getConfigSrcDir
    
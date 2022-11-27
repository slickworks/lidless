from .base import BaseEndToEnd


class TestBackup(BaseEndToEnd):
    def test_show(self):
        files = """
        foo
        foo/bar.txt
        foo/foo.txt
        """
        self.create_src_dir(files)
        # self.assert_dest(files)
        print(self.call("ls -al"))
        # self.call("show {self.target}")
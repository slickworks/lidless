from .base import BaseEndToEndWithTarget


class TestBackup(BaseEndToEndWithTarget):
    def test_show(self):
        files = """
        foo
        foo/bar.txt
        foo/foo.txt
        """
        self.create_src_dir(files)
        self.roots.update(self.create_root("foo", data={"tags": [self.target_tag]}))
        self.save_config()
        output = self.call(f"backup {self.target_key}")
        print(output)

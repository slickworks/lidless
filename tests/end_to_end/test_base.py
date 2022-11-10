from .base import EndToEndTest


class TestBaseClass(EndToEndTest):

    def test_base_class_methods(self):
        files = """
        foo
        foo/bar.txt
        """
        self.setSrcDir(files)
        self.setDestDir(files)
        self.assertDest(files)
    
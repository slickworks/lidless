import pytest
from .base import BaseEndToEnd, DEST_DIR, SRC_DIR


class TestBaseEndToEnd(BaseEndToEnd):
    """
    Testing the base class itself.
    """

    @pytest.fixture
    def fileset1(self):
        return """
        foo
        foo/bar.txt
        foo/foo.txt
        """

    @pytest.fixture
    def fileset2(self):
        return """
        foo
        foo/foo.txt
        bar
        """

    def test_clean_lines(self, fileset1, fileset2):
        assert self.clean_lines(fileset1) == ["foo", "foo/bar.txt", "foo/foo.txt"]
        assert self.clean_lines(fileset2) == ["bar", "foo", "foo/foo.txt"]

    def test_create_src_dir(self, fileset1):
        self.create_src_dir(fileset1)
        contents = self.read_dir_contents(SRC_DIR)
        assert contents == self.clean_lines(fileset1)

    def test_create_dest_dir(self, fileset1):
        self.create_dest_dir(fileset1)
        contents = self.read_dir_contents(DEST_DIR)
        assert contents == self.clean_lines(fileset1)

    def test_assert_dest_when_same(self, fileset1):
        self.create_src_dir(fileset1)
        self.create_dest_dir(fileset1)
        self.assert_dest(fileset1)

    def test_assert_dest_when_different(self, fileset1, fileset2):
        self.create_src_dir(fileset1)
        self.create_dest_dir(fileset2)
        with pytest.raises(AssertionError):
            self.assert_dest(fileset1)
        with pytest.raises(AssertionError):
            self.assert_dest("")

import pytest
from .base import BaseEndToEndWithTarget, DEST_DIR


class TestBackup(BaseEndToEndWithTarget):

    @pytest.fixture
    def root(self, fileset1):
        root = self.create_root("foo")
        self.create_src_dir(fileset1)
        self.roots[root] = {"tags": [self.target_tag]}
        self.save_config()
        return root

    def test_print_only(self, root):
        output = self.call(f"backup {self.target_key} --print-only")
        expected = [
            "rsync",
            root,
            DEST_DIR
        ]
        for s in expected:
            self.assert_output_contains(output, s)
        assert self.dest_contents() == []

    @pytest.mark.usefixtures("root")
    def test_no_prompt_syncs_contents_on_empty_dir(self, fileset1):
        assert self.dest_contents() == []
        self.call(f"backup {self.target_key} --no-prompt")
        assert self.dest_contents() == self.clean_lines(fileset1)

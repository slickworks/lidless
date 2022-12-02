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

    # def setup_method(self):
    #     super().setup_method()

    def test_print_cmd(self, root):
        output = self.call(f"backup {self.target_key} --print-only")
        expected = [
            "rsync",
            root,
            DEST_DIR
        ]
        for s in expected:
            assert s in output[0]
        assert "--dry-run" not in output[0]

    # def test_print_cmd_dry_run(self, root):
    #     output = self.call(f"backup {self.target_key} --cmds --dry-run")
    #     expected = [
    #         "rsync",
    #         root,
    #         DEST_DIR,
    #         "--dry-run" 
    #     ]
    #     for s in expected:
    #         assert s in output[0]
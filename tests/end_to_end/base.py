import os
import glob
import shutil
import subprocess

from lidless.utils import join_paths, create_file, create_dir
from tests.base import BaseAll, DEST_DIR, TMP_DIR, SRC_DIR, ROOT


class DirUtils:
    def clean_lines(self, file_list_str) -> list[str]:
        lines = []
        for line in file_list_str.split(os.linesep):
            line = line.strip()
            if len(line):
                lines.append(line)
        lines.sort()
        return lines

    def create_dir_contents(self, base, file_list_str) -> None:
        for line in self.clean_lines(file_list_str):
            path = join_paths(base, line)
            if "." in line:
                create_file(path, "foo")
            else:
                create_dir(path)

    def read_dir_contents(self, path) -> list[str]:
        lines = glob.glob("**/*", root_dir=path, recursive=True)
        lines.sort()
        return lines


class BaseEndToEnd(BaseAll, DirUtils):

    def setup_method(self):
        super().setup_method()
        os.makedirs(TMP_DIR, exist_ok=True)

    def save_config(self, check=True):
        config = self.get_config()
        if check:
            for node in config.get_nodes():
                if not node.path.startswith(SRC_DIR):
                    raise AssertionError(f"Node in config does not start with {SRC_DIR}:\
                        {os.linesep}    {node.path}")
        config.save()
            

    def teardown_method(self):
        shutil.rmtree(TMP_DIR)

    def create_src_dir(self, file_list_str):
        self.create_dir_contents(SRC_DIR, file_list_str)

    def create_dest_dir(self, file_list_str):
        self.create_dir_contents(DEST_DIR, file_list_str)

    def assert_dest(self, file_list_str):
        assert self.read_dir_contents(DEST_DIR) == self.clean_lines(file_list_str)

    def call(self, command):
        """Calls lidless and returns output as list of strings."""
        os.chdir(ROOT) 
        command = f"python -m lidless {command}"
        out = subprocess.getoutput(command)
        return out.split(os.linesep)



class BaseEndToEndWithTarget(BaseEndToEnd):
    """
    Remember to self.save_config() before self.call()
    """
    target_key = "ext"
    target_tag = "foo"

    def setup_method(self):
        super().setup_method()
        self.targets[self.target_key] = self.create_target(tags=[self.target_tag])
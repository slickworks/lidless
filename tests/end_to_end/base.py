import os
import glob
import shutil
import subprocess

from lidless.utils import join_paths, create_file, create_dir
from tests.base import BaseAll,CONFIG_FILE, DEST_DIR, TMP_DIR, SRC_DIR, ROOT


def local(path):
    return join(TMP_DIR, path)


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
        self.get_config().save()
        # with open(CONFIG_FILE, "w") as fp:
        #     json.dump(self.get_config(), fp)

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

import os
import glob
import pprint
import shutil
import subprocess

from lidless import Config
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

    def save_config(self):
        config = self.get_config()
        config.save()

    def teardown_method(self):
        shutil.rmtree(TMP_DIR)

    def create_src_dir(self, file_list_str):
        self.create_dir_contents(SRC_DIR, file_list_str)

    def create_dest_dir(self, file_list_str):
        self.create_dir_contents(DEST_DIR, file_list_str)

    def dest_contents(self):
        return self.read_dir_contents(DEST_DIR)

    def safety_check(self):
        """
        Checks the config as it will be loaded by command and ensures all collected
        directories are in TMP dir.
        """
        config = Config(TMP_DIR)

        def ensure(node, att, correct):
            value = getattr(node, att)
            if not value.startswith(correct):
                raise AssertionError(
                    f"Node {att} does not start with {correct}:\
                    {os.linesep}    {value}"
                )

        for target_key in config.target_keys():
            target = config.get_target(target_key)
            for node in target.nodes:
                ensure(node, "path", SRC_DIR)

    def call(self, command, check=True):
        """Calls lidless and returns output as list of strings."""
        os.chdir(ROOT)
        if check:
            self.safety_check()
        command = f"python -m lidless {command}"
        out = subprocess.getoutput(command)
        return out.split(os.linesep)

    def lines_contain(self, lines, contents):
        for line in lines:
            if contents in line:
                return True
        return False

    def assert_output_contains(self, output, contents):
        if not self.lines_contain(output, contents):
            lines = pprint.pformat(output)
            raise AssertionError(
                f"Output does not have expected contents.\n\
                Contents: '{contents}'.\n\
                Output: {lines}"
            )
        return output


class BaseEndToEndWithTarget(BaseEndToEnd):
    """
    Remember to self.save_config() before self.call()
    """

    target_key = "ext"
    target_tag = "foo"

    def setup_method(self):
        super().setup_method()
        self.targets[self.target_key] = self.create_target(tags=[self.target_tag])

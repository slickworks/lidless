import os
import subprocess
import sys

from dataclasses import dataclass
from lidless.exceptions import DataclassInitErr
from lidless.models import Change, Tool
from lidless.utils import get_src_and_dest, join_paths
from lidless import ui


class BaseTool(Tool):
    """
    Subclasses:
        - Must use @dataclass
        - Must specify own fields.
        - Must implement public methods using same signatures.
    """

    def _exec(self, cmd):
        subprocess.check_call(
            cmd, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT
        )

    def _getoutput(self, cmd):
        output = subprocess.getoutput(cmd)
        return output.split(os.linesep)

    def _exec_cmds(self, cmds, print_only=False):
        if print_only:
            func = print
        else:
            func = self._exec
        for cmd in cmds:
            func(cmd)


class RsyncBase(BaseTool):
    """
    Base class for rsync like tools.
    The backup and restore commands should be identical, just in different directions.

    Note: rsync is passed whole directories with trailing / on each, which allows src
    and dest paths to match.
    """

    maps: dict
    cmd: str

    def backup(self, nodes, no_prompt, print_only, diff_only):
        self._run(nodes, no_prompt, print_only, diff_only, False)

    def restore(self, nodes, no_prompt, print_only, diff_only):
        self._run(nodes, no_prompt, print_only, diff_only, True)

    def _run(self, nodes, no_prompt, print_only, diff_only, reverse):
        if print_only or diff_only:
            no_prompt = True

        if no_prompt:
            cmds = self._get_cmds(nodes, diff_only, reverse)
            self._exec_cmds(cmds, print_only)
        else:
            changes = self._get_changes(nodes, reverse)
            if ui.user_accepts_changes(changes):
                cmds = self._get_cmds(nodes, False, reverse)
                self._exec_cmds(cmds, print_only)

    def _get_cmds(self, nodes, diff_only, reverse):
        cmds = []

        if diff_only:
            opts = '-ain --out-format="%o %l %n"'
        else:
            opts = "-az"

        for node in nodes:
            src, dest = get_src_and_dest(node.path, self.maps, reverse)
            cmd = self._get_cmd(src=src, dest=dest, opts=opts)
            for ex in node.exclude:
                cmd += f" --exclude {ex}"
            cmds.append(cmd)

        return cmds

    def _get_changes(self, nodes, reverse):
        changes = []
        for node, cmd in zip(nodes, self._get_cmds(nodes, True, reverse)):
            for change_output in self._getoutput(cmd):
                if change_output:
                    action, size, path = change_output.split(" ", maxsplit=2)
                    path = join_paths(node.path, path)
                    changes.append(Change(action=action, size=int(size), path=path))
        return changes


@dataclass
class Rsync(RsyncBase):
    maps: dict
    cmd: str = "rsync {opts} --mkpath {src} {dest} --delete"


@dataclass
class Rclone(BaseTool):
    cmd = "rclone sync {src} {provider}:{dest}"
    provider: str

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts, provider=self.provider)


@dataclass
class Git(BaseTool):
    def backup(self, nodes, no_prompt, print_only, diff_only):
        pass

    def restore(self, nodes, no_prompt, print_only, diff_only):
        pass


config = {
    "rsync": Rsync,
    "rclone": Rclone,
}


def get_tool(data: dict) -> BaseTool:
    try:
        key = data.pop("tool")
    except KeyError:
        raise
    cls = config[key]
    try:
        return cls(**data)
    except TypeError as err:
        raise DataclassInitErr(key, err)

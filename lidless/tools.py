import os
import subprocess

from dataclasses import dataclass
from lidless.exceptions import DataclassInitErr


@dataclass
class BaseTool:
    """
    Subclasses:
        - Must implement public methods using same signatures.
        - May specify additional dataclass fields.
    """
    cmd = "echo {src} && echo {dest} && ech {opts}"

    def backup(self, src, dest, exclude, print_only, diff_only):
        pass

    def restore(self, src, dest, exclude, print_only, diff_only):
        pass

    def __str__(self):
        return f"{type(self).__name__}:{os.linesep}{super().__str__()}"

    def _run(self, command):
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts)


class RsyncBase(BaseTool):
    def backup(self, src, dest, exclude, print_only, diff_only):
        self._apply(src, dest, exclude, print_only, diff_only)
        
    def restore(self, src, dest, exclude, print_only, diff_only):
        self._apply(dest, src, exclude, print_only, diff_only)

    def _apply(self, src, dest, exclude, print_only, diff_only):
        opts = ""
        if diff_only:
            opts += " -avn"

        cmd = self._get_cmd(src=dest, dest=src, opts=opts)
        cmd = self._add_exclude(cmd, exclude)
        
        if print_only:
            print(cmd)
        else:
            self._run(cmd)
        
    def _add_exclude(self, cmd, exclude):
        for ex in exclude:
            cmd += f" --exclude {ex}"
        return cmd


@dataclass
class Rsync(RsyncBase):
    dest: str = ""
    cmd: str = "rsync -a {src} {dest} --delete-after"


@dataclass
class Rclone(BaseTool):
    cmd = "rclone sync {src} {provider}:{dest}"
    provider: str

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts, provider=self.provider)


class Git(BaseTool):

    def backup(self, src, dest, exclude, print_only, diff_only):
        pass
    
    def restore(self, src, dest, exclude, print_only, diff_only):
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
        return cls(*data)
    except TypeError as err:
        raise DataclassInitErr(key, err)

import os
import subprocess

from operator import itemgetter
from dataclasses import dataclass
from lidless.exceptions import DataclassInitErr


class BaseTool:
    """
    Subclasses:
        - Must use @dataclass
        - Must specify own fields.
        - Must implement public methods using same signatures.
    """
    cmd = "echo {src} && echo {dest} && ech {opts}"

    def backup(self, src, dest, exclude, print_only, diff_only):
        pass

    def restore(self, src, dest, exclude, print_only, diff_only):
        pass

    def __str__(self):
        return f"{type(self).__name__}:{os.linesep}{super().__str__()}"

    def _exec(self, command):
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts)


class RsyncBase(BaseTool):
    """
    Base class for rsync like tools.
    The backup and restore commands should be identical, just in different directions.
    """

    maps: dict
    dest: str
    cmd: str

    def backup(self, src, dest, exclude, print_only, diff_only):
        self._run(src, exclude, print_only, diff_only, True)
        
    def restore(self, src, dest, exclude, print_only, diff_only):
        self._run(src, exclude, print_only, diff_only, False)

    def _run(self, src, exclude, print_only, diff_only, backup):
        opts = ""
        if diff_only:
            opts += " -avn"

        src, dest = self._get_paths(src, backup)
        cmd = self._get_cmd(src=dest, dest=src, opts=opts)
        cmd = self._add_exclude(cmd, exclude)
        
        if print_only:
            print(cmd)
        else:
            self._exec(cmd)
        
    def _get_paths(self, path, backup):

        if backup:
            src = path
            dest = self._subs_path(path, False)
        else:
            src = self._subs_path(path, True)
            dest = path

        return src, dest

    def _subs_path(self, path, switch=False):
        for a, b in self._get_pairs(switch):
            if path.startswith(a):
                path = path[len(a):]
                return b + path
        
    def _get_pairs(self, switch=False):
        pairs = []
        for k, v in self.maps:
            if switch:
                pair = k, v
            else:
                pair = v, k
            pairs.append(pair)
        pairs.sort(key=itemgetter(0))
        return pairs

    def _add_exclude(self, cmd, exclude):
        for ex in exclude:
            cmd += f" --exclude {ex}"
        return cmd


@dataclass
class Rsync(RsyncBase):
    maps: dict
    dest: str = ""
    cmd: str = "rsync -a --mkpath {src} {dest} --delete-after"


@dataclass
class Rclone(BaseTool):
    cmd = "rclone sync {src} {provider}:{dest}"
    provider: str

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts, provider=self.provider)

@dataclass
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
        return cls(**data)
    except TypeError as err:
        raise DataclassInitErr(key, err)

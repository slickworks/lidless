from dataclasses import dataclass
from .base_rsync import RsyncBase


@dataclass
class Rsync(RsyncBase):
    maps: dict
    cmd: str = "rsync {opts} --mkpath {src} {dest} --delete"

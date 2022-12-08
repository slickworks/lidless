from dataclasses import dataclass
from .base_rsync import RsyncBase


@dataclass
class Rclone(RsyncBase):
    maps: dict
    cmd = "rclone sync {src} {provider}:{dest}"
    provider: str

    def _get_cmd(self, src, dest, opts):
        return self.cmd.format(src=src, dest=dest, opts=opts, provider=self.provider)

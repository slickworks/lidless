from lidless.exceptions import DataclassInitErr
from lidless.models import Tool
from .git import Git
from .rclone import Rclone
from .rsync import Rsync


config = {
    "git": Git,
    "rsync": Rsync,
    "rclone": Rclone,
}


def get_tool(data: dict) -> Tool:
    try:
        key = data.pop("tool")
    except KeyError:
        raise
    cls = config[key]
    try:
        return cls(**data)
    except TypeError as err:
        raise DataclassInitErr(key, err)

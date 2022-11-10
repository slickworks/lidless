"""

"""
from lidless import ui
from lidless.config import Config


def configure():
    """
    """


def check_repos(config):
    """
    Reports on status of all repos.
    """


def cmd_backup(config, remote_keys):
    """
    """
    for key in remote_keys:
        remote = config.get_remote(key)
        remote.find_changes()
        if ui.accept_changes(remote):
            remote.sync()


def main():
    config = Config()
    cmd_backup(config, remote_keys=["mega"])


if __name__ == "__main__":
    main()
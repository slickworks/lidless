from lidless import ui
# from lidless.config import Config


def config():
    """
    Handle configure options
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


# def main():
#     config = Config()
#     cmd_backup(config, remote_keys=["mega"])


def show(target):
    """
    Shows collection data.
    """

def changes(target):
    """
    Shows changes.
    """

def backup(target):
    """
    Runs backup.
    """

def restore(target):
    """
    Runs restore.
    """
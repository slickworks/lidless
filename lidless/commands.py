from lidless import ui

# from lidless.config import Config


def cmd_backup(config, remote_keys):
    """ """
    for key in remote_keys:
        remote = config.get_remote(key)
        remote.find_changes()
        if ui.accept_changes(remote):
            remote.sync()

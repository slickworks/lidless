from lidless import ui
from lidless.config import Config


class BaseCommand:
    cmd_name = ""
    cmd_help = "No help provided"
    
    def __init__(self, config: Config) -> None:
        self.config = config

    def register(self, subparsers):
        sub_parser = subparsers.add_parser(self.cmd_name, help=self.cmd_help)
        sub_parser.set_defaults(call=self.call)
        self.add_arguments(sub_parser)

    def add_arguments(self, parser):
        pass

    def call(self, args):
        print(f"running {self.cmd_name}")
        print(args.__dict__)

    def _run_tool_func(self, target_key, func, args):
        target = self.config.get_target(target_key)
        call = getattr(target, func)
        for node in target.nodes:
            call(node)


class ConfigCommand(BaseCommand):
    cmd_name = "config"
    cmd_help = "Do config stuff"


class BaseTargetCommand(BaseCommand):
    """Base for commands which run against targets."""
    def add_arguments(self, parser):
        parser.add_argument("target", help="Name of target")


class BackupCommand(BaseTargetCommand):
    cmd_name = "backup"
    cmd_help = "Runs backup"

    def call(self, args):
        target_key = args.target
        target = self.config.get_target(target_key)
        tool = target.tool
        if target.nodes:
            for node in target.nodes:
                tool.backup(node.path, node.dest, node.exclude)
        else:
            print("No nodes collected.")
        # for key in remote_keys:
        #     remote = self.config.get_remote(key)
        #     remote.find_changes()
        #     if ui.accept_changes(remote):
        #         remote.sync()


"""
show changes backup restore.
"""


class RestoreCommand(BaseTargetCommand):
    cmd_name = "restore"
    cmd_help = "Runs restores"


commands = [
    ConfigCommand,
    BackupCommand,
    RestoreCommand,
]
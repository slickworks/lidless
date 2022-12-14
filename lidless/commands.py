import os
from lidless.config import Config
from lidless import ui


class BaseCommand:
    cmd_name = ""
    cmd_help = "No help provided"

    def __init__(self, config: Config) -> None:
        self.config = config

    def register(self, subparsers):
        sub_parser = subparsers.add_parser(self.cmd_name, help=self.cmd_help)
        sub_parser.set_defaults(call=self.call)
        self._add_arguments(sub_parser)

    def call(self, args):
        raise NotImplementedError()

    def _add_arguments(self, parser):
        pass


class CwdCommand(BaseCommand):
    cmd_name = "cwd"
    cmd_help = "Do config stuff"

    def call(self, args):
        cwd = os.getcwd()
        node = self.config.get_node(cwd)
        if ui.edit_node(node):
            node.save()
            self.config.save()


class BaseTargetCommand(BaseCommand):
    """
    Base for commands which run against targets.

    The default behaviour is to show changes and prompt whether to continue,
    but this can be overriden with optional arguments.
    """

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.nodes = []

    def _add_arguments(self, parser):
        parser.add_argument("target", help="Name of target")
        parser.add_argument(
            "--diff-only", action="store_true", help="Show the changes, don't run."
        )
        parser.add_argument(
            "--print-only", action="store_true", help="Print commands, don't run."
        )
        parser.add_argument(
            "--no-prompt",
            action="store_true",
            help="Don't prompt to confirm changes, just run.",
        )

    def call(self, args):
        target_key = args.target
        target = self.config.get_target(target_key)
        nodes = target.nodes
        if nodes:
            func = getattr(target.tool, self.cmd_name)
            func(
                nodes=nodes,
                no_prompt=args.no_prompt,
                print_only=args.print_only,
                diff_only=args.diff_only,
            )
        else:
            ui.out("No nodes selected.")


class BackupCommand(BaseTargetCommand):
    cmd_name = "backup"
    cmd_help = "Backup files from source to dest"


class RestoreCommand(BaseTargetCommand):
    cmd_name = "restore"
    cmd_help = "Restore files from dest to source"


commands = [
    CwdCommand,
    BackupCommand,
    RestoreCommand,
]

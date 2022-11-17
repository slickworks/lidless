from lidless.config import Config


class Controller:

    target_cmds = [
        "cmd_show",
        "cmd_changes",
        "cmd_backup",
        "cmd_restore",
    ]

    def __init__(self, config: Config) -> None:
        self.config = config

    def cmd_config(self, args):
        """
        Handle configure options
        """

    def cmd_show(self, args):
        """
        Shows collection data.
        """
        self._run_tool_func(args.target, "show", args)

    def cmd_changes(self, args):
        """
        Shows changes.
        """

    def cmd_backup(self, args):
        """
        Runs backup.
        """

    def cmd_restore(self, args):
        """
        Runs restore.
        """

    def _run_tool_func(self, target_key, func, args):
        target, nodes = self.config.get_target_and_nodes(target_key)
        call = getattr(target.tool, func)
        for node in nodes:
            call(node)



        # def get_exclude_file(self, path, exclude):
        #     pass

        # def _save(self):
        #     with open(self.config_file, "w") as fp:
        #         json.dump(self.__data, fp, indent=4)

        # def add_target(self, name, cmd):
        #     self.data["targets"][name] = {"cmd": cmd}
        #     self._save()

        # def add_node(self, path):
        #     pass

        # def add_repo(self, path):
        pass

from lidless.models import Change
from lidless.utils import get_src_and_dest, join_paths
from lidless import ui
from .base_tool import BaseTool


class RsyncBase(BaseTool):
    """
    Base class for rsync like tools.
    The backup and restore commands should be identical, just in different directions.

    Note: rsync is passed whole directories with trailing / on each, which allows src
    and dest paths to match.
    """

    maps: dict
    cmd: str

    def backup(self, nodes, no_prompt, print_only, diff_only):
        self._run(nodes, no_prompt, print_only, diff_only, False)

    def restore(self, nodes, no_prompt, print_only, diff_only):
        self._run(nodes, no_prompt, print_only, diff_only, True)

    def _run(self, nodes, no_prompt, print_only, diff_only, reverse):
        if print_only or diff_only:
            no_prompt = True

        if no_prompt:
            cmds = self._get_cmds(nodes, diff_only, reverse)
            self._exec_cmds(cmds, print_only)
        else:
            changes = self._get_changes(nodes, reverse)
            if ui.user_accepts_changes(changes):
                cmds = self._get_cmds(nodes, False, reverse)
                self._exec_cmds(cmds, print_only)

    def _get_cmds(self, nodes, diff_only, reverse):
        cmds = []

        if diff_only:
            # Use %n rather than %f as %f prints full path for "send" but 
            # relative paths for "del." entries. We join the base path later.
            opts = '-ain --out-format="%o %l %n"'
        else:
            opts = "-az"

        for node in nodes:
            src, dest = get_src_and_dest(node.path, self.maps, reverse)
            cmd = self._get_cmd(src=src, dest=dest, opts=opts)
            for ex in node.exclude:
                cmd += f" --exclude {ex}"
            cmds.append(cmd)

        return cmds

    def _get_changes(self, nodes, reverse):
        changes = []
        for node, cmd in zip(nodes, self._get_cmds(nodes, True, reverse)):
            for change_output in self._get_output(cmd):
                if change_output:
                    action, size, path = change_output.split(" ", maxsplit=2)
                    path = join_paths(node.path, path)
                    changes.append(Change(action=action, size=int(size), path=path))
        return changes

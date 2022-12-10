from typing import Optional

from lidless import ui
from lidless.models import Actions, Change
from lidless.utils import get_src_and_dest, convert_size, get_path_leaves
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
            if self._accept_changes(nodes, reverse):
                cmds = self._get_cmds(nodes, False, reverse)
                self._exec_cmds(cmds, print_only)

    def _get_cmds(self, nodes, diff_only, reverse):
        cmds = []
        opts = self._get_cmd_opts(diff_only, reverse)

        for node in nodes:
            src, dest = get_src_and_dest(node.path, self.maps, reverse)
            cmd = self._get_cmd(src=src, dest=dest, opts=opts)
            for ex in node.exclude:
                cmd += f" --exclude {ex}"
            cmds.append(cmd)

        return cmds

    def _get_cmd_opts(self, diff_only, reverse):
        raise NotImplementedError()

    def _accept_changes(self, nodes, reverse):        
        changes = self._get_changes(nodes, reverse)
        if not (changes):
            ui.out("")
            ui.out(" No changes detected.")
            ui.out("")
            return False

        self.print_changes_summary(changes)
        if ui.prompt_yn("Do you want to list them?"):
            ui.out("---------------------------------------------")
            ui.out("")
            for change in sorted(changes, key=lambda c: c.path):
                ui.out(change)
            ui.out("")

        return ui.prompt_yn("Do you want to proceed?")

    def print_changes_summary(self, changes):
        total_size = convert_size(sum(c.size for c in changes))
        directories = get_path_leaves(c.path for c in changes)
        copy = [c for c in changes if c.action == Actions.copy]
        delete = [c for c in changes if c.action == Actions.delete]
        unknown = [c for c in changes if c.action == Actions.unknown]

        ui.out("-------------------CHANGES-------------------")
        ui.out("")

        # actions = set(c.action for c in changes)
        # for action in actions:
        #     these = [c for c in changes if c.action == action]
        #     ui.out(f" {action}: {len(these)}")

        ui.out(f" Copy: {len(copy)}")
        ui.out(f" Delete: {len(delete)}")
        ui.out(f" Other: {len(unknown)}")

        #  ({total_size})

        ui.out(
            f" {len(copy)} changes ({total_size}) and {len(delete)}\
                deletions in {len(directories)} directories:"
        )
        ui.out("")
        for d in directories:
            ui.out(f"    {d}")
        ui.out("")

    def _get_changes(self, nodes, reverse):
        changes = []
        for node, cmd in zip(nodes, self._get_cmds(nodes, True, reverse)):
            for output in self._get_output(cmd):
                change = self._parse_output(node, output)
                if change:
                    changes.append(change)
        return changes

    def _parse_output(self, nodes, output) -> Optional[Change]:
        raise NotImplementedError()
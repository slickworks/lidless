import os
from dataclasses import dataclass
from lidless.models import GitChanges
from .base_tool import BaseTool


@dataclass
class Git(BaseTool):
    def backup(self, nodes, no_prompt, print_only, diff_only):
        """
        Only does diff.
        """
        if any([no_prompt, print_only, diff_only]):
            print("Options ignored.")

        cmd_other = "git log --branches --not --remotes --decorate --oneline"
        cmd_diff = "git diff --name-only"
        cmd_diff_cached = "git diff --name-only --cached"
        changes = []
        for node in nodes:
            os.chdir(node.path)
            uncommitted = self._get_output(cmd_diff) + self._get_output(cmd_diff_cached)
            unpushed = self._get_output(cmd_other)
            if uncommitted or unpushed:
                changes.append(GitChanges(
                    path=node.path,
                    uncommitted=uncommitted,
                    unpushed=unpushed
                ))
        if changes:
            for change in changes:
                print(change)
            print("")
        else:
            print(f"No unsaved changes across {len(nodes)} repos.")
        
    def restore(self, nodes, no_prompt, print_only, diff_only):
        print("Not implemented yet")

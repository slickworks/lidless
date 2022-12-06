import os
from dataclasses import dataclass
from .base_tool import BaseTool


@dataclass
class GitChanges:
    path: str
    uncommitted: list[str]
    unpushed: list[str]

    def __str__(self):
        lines = [f"{os.linesep}  {self.path}"]
        if self.uncommitted:
            lines.append("    Uncommitted changes:")
            lines.extend(f"      {s}" for s in self.uncommitted)
        if self.unpushed:
            lines.append("    Unpushed commits:")
            lines.extend(f"      {s}" for s in self.unpushed)
        return os.linesep.join(lines)

@dataclass
class Git(BaseTool):
    def backup(self, nodes, no_prompt, print_only, diff_only):
        """
        Only does diff.
        """
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
        

    def restore(self, nodes, no_prompt, print_only, diff_only):
        pass

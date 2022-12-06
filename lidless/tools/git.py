from dataclasses import dataclass
from .base_tool import BaseTool


@dataclass
class Git(BaseTool):
    def backup(self, nodes, no_prompt, print_only, diff_only):
        pass

    def restore(self, nodes, no_prompt, print_only, diff_only):
        pass

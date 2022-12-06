import os
import subprocess
import sys

from lidless.models import Tool


class BaseTool(Tool):
    """
    Subclasses:
        - Must use @dataclass
        - Must specify own fields.
        - Must implement public methods using same signatures.
    """

    def _exec(self, cmd):
        subprocess.check_call(
            cmd, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT
        )

    def _get_output(self, cmd):
        output = subprocess.getoutput(cmd)
        return output.split(os.linesep)

    def _exec_cmds(self, cmds, print_only=False):
        if print_only:
            func = print
        else:
            func = self._exec
        for cmd in cmds:
            func(cmd)
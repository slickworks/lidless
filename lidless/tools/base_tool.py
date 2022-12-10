import os
import subprocess
import sys

from lidless.models import Tool


class BaseTool(Tool):

    def _exec(self, cmd):
        subprocess.check_call(
            cmd, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT
        )

    def _get_output(self, cmd):
        output = subprocess.getoutput(cmd)
        lines = output.split(os.linesep)
        if len(lines) == 1 and lines[0] == "":
            return []
        return lines

    def _exec_cmds(self, cmds, print_only=False):
        if print_only:
            func = print
        else:
            func = self._exec
        for cmd in cmds:
            func(cmd)
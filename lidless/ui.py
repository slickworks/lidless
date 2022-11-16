import sys
from lidless.models import Target

def accept_changes(target):
    print(target.changes)


def error(msg):
    print(msg)
    sys.exit(1)
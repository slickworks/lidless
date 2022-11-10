import sys
from lidless.models import Remote

def accept_changes(remote: Remote):
    print(remote.changes)


def error(msg):
    print(msg)
    sys.exit(1)
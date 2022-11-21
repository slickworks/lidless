import sys
from lidless.target import Target


def accept_changes(target):
    print(target.changes)


def error(msg):
    print(msg)
    sys.exit(1)

from os.path import dirname
import sys
from lidless.utils import convert_size, get_path_leaves


def user_accepts_changes(changes):

    if not (changes):
        print("")
        print(" No changes detected.")
        print("")
        return False

    print_changes_summary(changes)
    if prompt_yn("Do you want to list them?"):
        print("---------------------------------------------")
        print("")
        for change in sorted(changes, key=lambda c: c.path):
            print(change)
        print("")

    return prompt_yn("Do you want to proceed?")


def print_changes_summary(changes):
    total_size = convert_size(sum(c.size for c in changes))
    directories = get_path_leaves(c.path for c in changes)
    send = [c for c in changes if c.action == "send"]
    delete = [c for c in changes if c.action == "del."]

    print("-------------------CHANGES-------------------")
    print("")
    print(
        f" {len(send)} changes ({total_size}) and {len(delete)}\
            deletions in {len(directories)} directories:"
    )
    print("")
    for d in directories:
        print(f"    {d}")
    print("")


def error(msg):
    print(msg)
    sys.exit(1)


def prompt_yn(msg):
    while True:
        try:
            print("> " + msg + " (y/n)")
            selection = input("> ").lower()[0]
            assert selection in ("y", "n")
            return selection == "y"
        except KeyboardInterrupt:
            quit()
        except AssertionError:
            print("Enter y or n:")

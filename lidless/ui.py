import sys
import readline

from lidless.utils import convert_size, get_path_leaves

prompt_symbol = "> "


def error(msg):
    print(msg)
    sys.exit(1)


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


def prompt_yn(msg):
    while True:
        try:
            print(prompt_symbol + msg + " (y/n)")
            selection = input(prompt_symbol).lower()[0]
            assert selection in ("y", "n")
            return selection == "y"
        except KeyboardInterrupt:
            quit()
        except AssertionError:
            print("Enter y or n:")


def space_join(items):
    return " ".join(sorted(items))


def space_split(items):
    return [s for s in sorted(items.split(" ")) if len(s)]


def edit_node(node):
    while True:
        tag_str = space_join(node.tags)
        exclude_str = space_join(node.exclude)
        print(node.path)
        print(f"  Tags: {tag_str}")
        print(f"  Exclude: {exclude_str}")
        print("")
        if prompt_yn("Edit tags?"):
            tag_str = prompt_text("New tags:", tag_str)
            node.tags = space_split(tag_str)
        if prompt_yn("Edit exclude?"):
            exclude_str = prompt_text("New exclude:", exclude_str)
            node.exclude = space_split(exclude_str)
        if prompt_yn("All done?"):
            break
    return prompt_yn("Save changes?")


def prompt_text(msg, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        print(prompt_symbol + msg)
        return input(prompt_symbol)
    finally:
        readline.set_startup_hook()
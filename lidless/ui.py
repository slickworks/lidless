import sys
import readline

prompt_symbol = "> "


def out(*msg):
    print(*msg)


def error(msg):
    out(msg)
    sys.exit(1)


def prompt_yn(msg):
    while True:
        try:
            out(prompt_symbol + msg + " (y/n)")
            selection = input(prompt_symbol).lower()[0]
            assert selection in ("y", "n")
            return selection == "y"
        except KeyboardInterrupt:
            quit()
        except AssertionError:
            out("Enter y or n:")


def space_join(items):
    return " ".join(sorted(items))


def space_split(items):
    return [s for s in sorted(items.split(" ")) if len(s)]


def edit_node(node):
    while True:
        tag_str = space_join(node.tags)
        exclude_str = space_join(node.exclude)
        out(node.path)
        out(f"  Tags: {tag_str}")
        out(f"  Exclude: {exclude_str}")
        out("")
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
        out(prompt_symbol + msg)
        return input(prompt_symbol)
    finally:
        readline.set_startup_hook()
"""
The entry point. You probably want to:

    python -m lidless {args}

"""
from argparse import ArgumentParser
from lidless.commands import backup, changes, config, restore, show


TARGET_CMDS = {
    "show": show,
    "changes": changes,
    "backup": backup,
    "restore": restore,
}


def main():
    parser = ArgumentParser(prog = "<your-alias>")
    parser.set_defaults(func=lambda _: parser.print_usage())
    subparsers = parser.add_subparsers()

    target_parser = ArgumentParser(add_help=False)
    target_parser.add_argument("target", help="Name of target")

    def add_sub_parser(func, name, parents):
        sub_parser = subparsers.add_parser(name, help=func.__doc__, parents=parents)
        sub_parser.set_defaults(func=func)
        return sub_parser

    config_parser = add_sub_parser(config, "config", [])
    # TODO: add options for setting tags on cwd etc.

    for name, func in TARGET_CMDS.items():
        add_sub_parser(func, name, [target_parser])

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
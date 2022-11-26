"""
The entry point. You probably want to:

    python -m lidless {args}

"""
from argparse import ArgumentParser
from lidless.config import Config
from lidless.exceptions import UserError
from lidless.ui import error
from lidless.commands import commands


def main(commands):
    config = Config()

    parser = ArgumentParser(prog="<your-alias>")
    parser.set_defaults(call=lambda _: parser.print_usage())
    subparsers = parser.add_subparsers()

    for cmd_cls in commands:
        cmd = cmd_cls(config)
        cmd.register(subparsers)

    args = parser.parse_args()

    try:
        args.call(args)
    except UserError as err:
        error(err)


if __name__ == "__main__":
    main(commands)

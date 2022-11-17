"""
The entry point. You probably want to:

    python -m lidless {args}

"""
from argparse import ArgumentParser
from lidless.config import Config
from lidless.controller import Controller
from lidless.exceptions import UserError
from lidless.ui import error


def main():
    config = Config()
    controller = Controller(config)

    parser = ArgumentParser(prog="<your-alias>")
    parser.set_defaults(func=lambda _: parser.print_usage())
    subparsers = parser.add_subparsers()

    target_parser = ArgumentParser(add_help=False)
    target_parser.add_argument("target", help="Name of target")

    def add_sub_parser(func, name, parents):
        sub_parser = subparsers.add_parser(name, help=func.__doc__, parents=parents)
        sub_parser.set_defaults(func=func)
        return sub_parser

    # config_parser = add_sub_parser(controller.cmd_config, "config", [])
    # TODO: add options for setting tags on cwd etc.

    for cmd_name in controller.target_cmds:
        func = getattr(controller, cmd_name)
        add_sub_parser(func, cmd_name[4:], [target_parser])

    args = parser.parse_args()

    try:
        args.func(args)
    except UserError as err:
        error(err)


if __name__ == "__main__":
    main()

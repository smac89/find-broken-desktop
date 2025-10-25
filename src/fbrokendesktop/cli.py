import argparse


class Cli(argparse.Namespace):
    user: bool = False
    hidden: bool = False
    delete: bool = False

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser(description="Find desktop entry files (*.desktop) with broken executables.")
        parser.add_argument(
            "--hidden",
            "--show_hidden",
            action="store_true",
            help="show hidden (aka NoDisplay) desktop entries",
            default=False,
        )
        parser.add_argument(
            "-d",
            "--delete",
            action="store_true",
            help="delete the missing entries",
            default=False,
        )
        parser.add_argument(
            "-u",
            "--user",
            action="store_true",
            help="list only the entries which are owned by the current user",
            default=False,
        )
        return parser.parse_args(namespace=cls())

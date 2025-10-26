import argparse
import pathlib

try:
    from fbrokendesktop._version import __version__
except ImportError:
    __version__ = "unknown"


class Args(argparse.Namespace):  # https://docs.python.org/3/library/argparse.html#the-namespace-object
    user: bool
    hidden: bool
    delete: bool
    debug: bool
    prompt: bool
    paths: list[pathlib.Path]

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser(description="Find desktop entry files (*.desktop) with broken executables.")
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"%(prog)s {__version__ if __version__.startswith('v') or __version__ == 'unknown' else f'v{__version__}'}",
        )
        parser.add_argument(
            "--hidden",
            "--show-hidden",
            action="store_true",
            help="show hidden (aka NoDisplay) desktop entries",
            default=False,
        )
        parser.add_argument(
            "-x",
            "--delete",
            action="store_true",
            help="delete the missing entries",
            default=False,
        )
        parser.add_argument(
            "--prompt",
            action=argparse.BooleanOptionalAction,
            help="prompt for confirmation before deleting",
            default=True,
        )
        parser.add_argument(
            "-u",
            "--user",
            action="store_true",
            help="list only the entries which are owned by the current user",
            default=False,
        )
        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="enable debug logging",
            default=False,
        )
        parser.add_argument(
            "paths",
            type=pathlib.Path,
            nargs=argparse.REMAINDER,
            help="(optional) directories/files to search for missing desktop entries",
        )
        return parser.parse_args(namespace=cls())

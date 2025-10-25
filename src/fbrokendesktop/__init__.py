import logging
import os

from fbrokendesktop import cli


def main(args: cli.Cli | None = None):
    """
    Main entry point. If args is None, use the default arguments
    """
    from fbrokendesktop import core

    if args is None:
        logging.info("Using default arguments")
        args = cli.Cli()

    for d in core.find_desktop_directories():
        for df in core.find_missing_desktop_files(d, args.hidden):
            if args.user and not os.access(df, os.W_OK | os.R_OK):
                continue
            if args.delete:
                os.remove(df)
                logging.info(f"Deleted {df}")
            else:
                print(df)

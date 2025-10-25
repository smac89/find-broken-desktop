import logging
import os

from fbrokendesktop import cli


def main(args: cli.Args | None = None):
    """
    Main entrypoint.
    """
    from fbrokendesktop import core

    if args is None:
        logging.info("Using default arguments")
        args = cli.Args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        style="{",
        format="{levelname}:\t[{asctime} {name}] {message}",
        datefmt=logging.Formatter.default_time_format,
    )

    logging.info("==> Finding broken desktop files. This might take a while... <==")
    broken_files: list[str] = []

    for d in core.find_desktop_directories():
        logging.debug(f"Searching in directory: {d}...")
        for df in core.find_missing_desktop_files(d, args.hidden):
            if args.user and not os.access(df, os.W_OK | os.R_OK):
                continue
            broken_files.append(df)

    if not broken_files:
        logging.info("No broken desktop entries found.")
        return

    logging.info(f"Found {len(broken_files)} broken desktop entries:")
    if args.delete:
        logging.info("Deleting files...")
        for df in broken_files:
            os.remove(df)
            logging.info(f"Deleted {df}")
    else:
        print(os.linesep.join(broken_files))


def __run():
    logging.root.name = __name__
    main(cli.Args.parse_args())

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

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info("==> Finding broken desktop files. This might take a while... <==")
    broken_files: list[str] = []

    for d in args.dir_paths or core.find_desktop_directories():
        logging.debug(f"Searching in directory: {d}...")
        for df in core.find_missing_desktop_files(d, args.hidden):
            if args.user and not os.access(df, os.W_OK | os.R_OK):
                continue
            broken_files.append(df)

    for f in args.file_paths:
        if file_name := core.check_invalid_desktop_entry(f, args.hidden):
            broken_files.append(file_name)

    if not broken_files:
        logging.info("No broken desktop entries found.")
        return

    logging.info(f"Found {len(broken_files)} broken desktop entries:")
    if args.delete:
        for df in broken_files:
            if args.prompt:
                match input(f"Delete {df}? [y/Y(all),n/N(cancel)] "):
                    case "N" | "NO" | "No":
                        return
                    case all if all.startswith("Y") and all.upper() in ("Y", "YE", "YES"):
                        args.prompt = False
                    case yes if yes.startswith("y") and yes.lower() in ("y", "ye", "yes"):
                        pass
                    case _:
                        logging.info(f"Skipped {df}")
                        continue
            os.remove(df)
            logging.info(f"Deleted {df}")
    else:
        print(os.linesep.join(broken_files))


def __run():
    logging.root.name = __name__
    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="{levelname}:\t[{asctime} {name}] {message}",
        datefmt=logging.Formatter.default_time_format,
    )
    main(cli.Args.parse_args())

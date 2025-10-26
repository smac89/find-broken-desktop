import logging
import os
import pathlib
import typing as t

if t.TYPE_CHECKING:
    from collections.abc import Iterable

from fbrokendesktop import cli, core


def main(args: cli.Args | None = None):
    """
    Main program.

    :param args: command line arguments
    """
    if args is None:
        logging.info("Using default arguments")
        args = cli.Args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.info("==> Finding broken desktop files. This might take a while... <==")

    broken_files = list(
        find_broken_entries(args.paths if args.paths else map(pathlib.Path, core.find_desktop_directories()))
    )

    if not broken_files:
        logging.info("No broken desktop entries found.")
        return

    logging.info(f"Found {len(broken_files)} broken desktop entries.")
    if args.delete:
        delete_count = delete_entries(broken_files, args.prompt)
        if delete_count == len(broken_files):
            logging.info("Deleted all broken desktop entries.")
        elif delete_count > 0:
            logging.info(f"Deleted {delete_count} of {len(broken_files)} broken desktop entries.")
        else:
            logging.info("No broken desktop entries deleted.")
    else:
        print(os.linesep.join(broken_files))


def delete_entries(to_delete: "Iterable[str | pathlib.Path]", prompt: bool = True):
    count_deleted = 0
    for desktop in to_delete:
        if prompt:
            match input(f"Delete {desktop}? [y/A(all),n/(cancel)] "):
                case "N" | "NO" | "No":
                    return count_deleted
                case all if all.startswith("Y") and all.upper() in ("Y", "YE", "YES"):
                    prompt = False
                case yes if yes.startswith("y") and yes.lower() in ("y", "ye", "yes"):
                    pass
                case _:
                    logging.debug(f"Skipped {desktop}")
                    continue
        os.remove(desktop)
        count_deleted += 1
        logging.debug(f"Deleted {desktop}")

    return count_deleted


def find_broken_entries(paths: "Iterable[pathlib.Path]"):
    for path in paths:
        if path.is_dir():
            for file_name in core.find_missing_desktop_files_in_dir(str(path), False):
                yield file_name
        elif path.is_file():
            if file_name := core.check_invalid_desktop_entry(str(path), False):
                yield file_name
        else:
            logging.warning(f"Skipping invalid path: {path}")

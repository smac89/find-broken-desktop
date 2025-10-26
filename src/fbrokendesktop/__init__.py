import logging

from fbrokendesktop import cli


def run():
    from fbrokendesktop.main import main

    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="{levelname}:\t[{asctime} {name}] {message}",
        datefmt=logging.Formatter.default_time_format,
    )
    logging.root.name = __name__
    main(cli.Args.parse_args())

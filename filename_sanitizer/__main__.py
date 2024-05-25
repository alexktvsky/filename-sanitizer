#!/usr/bin/env python3

import argparse

from filename_sanitizer import __version__
from filename_sanitizer.filename_sanitizer import FilenameSanitizer


DEFAULT_SEPARATOR = '_'
REPL_SEPARATOR = '->'


def get_version_info() -> str:
    return f'filename-sanitizer {__version__}'


def split_by_repl_separator(repl: str) -> list[str]:
    if REPL_SEPARATOR not in repl:
        raise RuntimeError(f'Replacements must be of the form: ORIGINAL{REPL_SEPARATOR}REPLACED')
    return repl.split(REPL_SEPARATOR, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-s', '--separator', type=str,
                        default=DEFAULT_SEPARATOR,
                        help='Separator between words')
    parser.add_argument('-l', '--lowercase', action='store_true',
                        default=False,
                        help='Transform text to lowercase')
    parser.add_argument('-r', '--recursive', action='store_true',
                        default=False, help='Process directory recursively')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help='Explain what is being done')
    parser.add_argument('--replacements', nargs='+', default=None,
                        help='Additional replacement rules e.g. ",-> and "')
    parser.add_argument('-V', '--version', action='version',
                        version=get_version_info(),
                        help='Print version information')

    args = parser.parse_args()

    if args.replacements:
        args.replacements = [
            split_by_repl_separator(repl) for repl in args.replacements
        ]

    fs = FilenameSanitizer(args.separator, args.replacements, args.lowercase,
                           args.verbose)

    if args.recursive:
        fs.process_directory(args.path)
    else:
        fs.process_path(args.path)


if __name__ == '__main__':
    main()

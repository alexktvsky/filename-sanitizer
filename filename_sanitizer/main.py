#!/usr/bin/env python3

import os
import csv
from typing import List
from argparse import ArgumentParser

from filename_sanitizer.filename_sanitizer import FilenameSanitizer
from filename_sanitizer.replace_table_item import ReplaceTableItem
from filename_sanitizer import __version__


def _get_version():
    return 'filename-sanitizer v.{}'.format(__version__)


def _read_additional_table(path: str) -> List[ReplaceTableItem]:
    with open(path, 'r') as fin:
        cin = csv.reader(fin)
        table = [ReplaceTableItem(row[0], row[1]) for row in cin]
        return table


def _print_verbose_info(old_name: str, new_name: str) -> None:
    print('"{}" -> "{}"'.format(old_name, new_name))


def _prompt(old_name: str, new_name: str) -> str:
    _print_verbose_info(old_name, new_name)
    rv = input('Press enter or provide a new name: ')
    if rv != '':
        new_name = rv
    return new_name


def _rename(old_name: str, new_name: str, intvly: bool, verbose: bool) -> None:
    if intvly:
        new_name = _prompt(old_name, new_name)
    if verbose:
        _print_verbose_info(old_name, new_name)
    os.rename(old_name, new_name)


def _sanitize_filename(sanitizer: FilenameSanitizer, filename: str) -> None:
    print(sanitizer.sanitize(filename))


def _sanitize(
    sanitizer: FilenameSanitizer,
    filename: str,
    interactively: bool,
    verbose: bool
) -> None:
    _rename(filename, sanitizer.sanitize(filename), interactively, verbose)


def _sanitize_dir(
    sanitizer: FilenameSanitizer,
    dirname: str,
    interactively: bool,
    verbose: bool
) -> None:
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            old_name = os.path.join(root, name)
            new_name = os.path.join(root, sanitizer.sanitize(name))
            _rename(old_name, new_name, interactively, verbose)

        for name in dirs:
            old_name = os.path.join(root, name)
            new_name = os.path.join(root, sanitizer.sanitize(name))
            _rename(old_name, new_name, interactively, verbose)


def main():

    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-t', '--table', type=str, required=False, help='provide an additional table with replacement strings')  # noqa: E501
    parser.add_argument('-n', '--name', action='store_true', default=False, help='sanitize only filename')  # noqa: E501
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='sanitize directories recursively')  # noqa: E501
    parser.add_argument('-i', '--interactively', action='store_true', default=False, help='prompt before rename')  # noqa: E501
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='explain what is being done')  # noqa: E501
    parser.add_argument('-V', '--version', action='version', version=_get_version(), help='output version information and exit')  # noqa: E501

    args = parser.parse_args()

    _additional_table = None
    if args.table:
        _additional_table = _read_additional_table(args.table)

    sanitizer = FilenameSanitizer(_additional_table)

    if args.name:
        _sanitize_filename(sanitizer, args.filename)
        return

    if not args.recursive:
        _sanitize(sanitizer, args.filename, args.interactively, args.verbose)

    _sanitize_dir(sanitizer, args.filename, args.interactively, args.verbose)


if __name__ == '__main__':
    main()

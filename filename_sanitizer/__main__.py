#!/usr/bin/env python3

import sys
import os
import argparse

import filename_sanitizer
from filename_sanitizer import __version__


def get_version():
    return 'filename-sanitizer {}'.format(__version__)


def read_text_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def sanitize_filename(filename, separator, to_lower, table=None):
    filename = filename.replace('\'', '')
    cmd = 'echo \'{}\''.format(filename)
    cmd += ' | tr -d \'\\n\\r\''  # Remove new lines and tabs
    cmd += ' | tr -d \',()\''  # Remove columns, scopes

    if table:
        cmd += ' | sed -e \'{}\''.format(table)

    cmd += ' | tr \' \' \'{}\''.format(separator)  # Replace spaces
    cmd += ' | tr -cd \'[:alnum:]_.-\''

    if to_lower:
        cmd += ' | tr \'[:upper:]\' \'[:lower:]\''

    return os.popen(cmd).read()


def print_verbose_info(old_name: str, new_name: str) -> None:
    print('"{}" -> "{}"'.format(old_name, new_name))


def prompt(old_name: str, new_name: str) -> str:
    rv = input('Press enter or provide a new name: ')
    if rv != '':
        new_name = rv
    return new_name


def rename_file(
    old_name,
    new_name,
    interactively=False,
    verbose=False
):
    if interactively:
        print_verbose_info(old_name, new_name)
        new_name = prompt(old_name, new_name)
    if verbose:
        print_verbose_info(old_name, new_name)
    os.rename(old_name, new_name)


def rename_files_recursive(
    dirname,
    separator,
    to_lower,
    table=None,
    interactively=False,
    verbose=False
):
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            old_name = os.path.join(root, name)
            new_name = os.path.join(
                root, sanitize_filename(name, separator, to_lower, table))
            rename_file(old_name, new_name, interactively, verbose)

        for name in dirs:
            old_name = os.path.join(root, name)
            new_name = os.path.join(
                root, sanitize_filename(name, separator, to_lower, table))
            rename_file(old_name, new_name, interactively, verbose)


def get_data_files_path():
    data_files_path = os.path.dirname(filename_sanitizer.__file__) + '/data'
    return data_files_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-s', '--separator', type=str, default='_', help='word separator')  # noqa: E501
    parser.add_argument('-t', '--table', type=str, required=False, help='table with replacement strings')  # noqa: E501
    parser.add_argument('-f', '--file', action='store_true', default=False, help='parameter is a name of file or directory')  # noqa: E501
    parser.add_argument('-l', '--lower', action='store_true', default=False, help='transform text to lowercase')  # noqa: E501
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='sanitize directories and their contents recursively')  # noqa: E501
    parser.add_argument('-i', '--interactively', action='store_true', default=False, help='prompt before rename')  # noqa: E501
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='explain what is being done')  # noqa: E501
    parser.add_argument('-V', '--version', action='version', version=get_version(), help='output version information and exit')  # noqa: E501

    args = parser.parse_args()

    table = None
    if args.table:
        base_path = get_data_files_path()
        table_filename = os.path.join(base_path, args.table)
        table = read_text_file(table_filename)

    if not args.file:
        new_name = sanitize_filename(
            args.filename, args.separator, args.lower, table)
        print(new_name)
        return 0

    if args.recursive:
        rename_files_recursive(
            args.filename,
            args.separator,
            args.lower,
            table,
            args.interactively,
            args.verbose
        )
    else:
        new_name = sanitize_filename(
            args.filename, args.separator, args.lower, table)
        rename_file(args.filename, new_name, args.interactively, args.verbose)

    return 0


if __name__ == '__main__':
    sys.exit(main())

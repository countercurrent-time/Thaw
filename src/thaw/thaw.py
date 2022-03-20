import argparse
import pkg_resources
import sys
import subprocess
import os
from pathlib import Path

import yaml
import click

__version = '0.0.1'


def _err(err):
    return f'thaw: error: {err}'

def _dbg(err):
    return f'[DEBUG] {err}'

def is_problem_dir(dir_path):
    return (dir_path / 'config.yml').is_file() \
       and is_repository_dir(dir_path.parent)
def is_repository_dir(dir_path):
    return (dir_path / '.git').is_dir() \
       and is_all_repositories_dir(dir_path.parent)
def is_all_repositories_dir(dir_path):
    return (dir_path / 'compile_args.yml').is_file()

# dir of a single problem (a directory with config.yml)
def problem_dir():
    cwd = Path.cwd()
    if is_problem_dir(cwd):
        return cwd
    else:
        return False

# dir of a repository of problems (must be a git repository)
def repository_dir():
    cwd = Path.cwd()
    if is_problem_dir(cwd):
        return cwd.parent
    elif is_repository_dir(cwd):
        return cwd
    else:
        return False

# dif of all the repositories (a directory with compile_args.yml)
def all_repositories_dir():
    cwd = Path.cwd()
    if is_problem_dir(cwd):
        return cwd.parent.parent
    elif is_repository_dir(cwd):
        return cwd.parent
    elif is_all_repositories_dir(cwd):
        return cwd
    else:
        return False


def copy_data(file_name, dir_path):
    data = pkg_resources.resource_string(__name__, file_name)
    with open(dir_path / file_name, 'wb') as target_file:
        target_file.write(data)

def parse_yaml(path_to_yaml_file):
    with Path(path_to_yaml_file).open() as file:
        return yaml.safe_load(file)

# init the directory of all the repositories by adding a compile_args.yml
def init(args):
    try:
        args.dir_path.mkdir(exist_ok=True)
    except FileNotFoundError:
        raise
    except FileExistsError:
        raise
    else:
        copy_data('compile_args.yml', args.dir_path)

# new a single problem by adding a config.yml
def new(args):
    try:
        args.dir_path.mkdir(exist_ok=True)
    except FileNotFoundError:
        raise
    except FileExistsError:
        raise
    else:
        copy_data('config.yml', args.dir_path)

# submit a code by executing the checker.py.
# TODO: still compatible to other problems without checker.py
def submit(args):
    checker = args.code.parent / 'checker.py'
    if checker.is_file():
        subprocess.run(
            ['python3', str(args.code.parent / 'checker.py')] + sys.argv[2:],
            stdout=sys.stdout,
            stderr=sys.stderr
        )

# used for type checking and type conversion when parsing arguments.
class StrictPath:
    def __call__(self, arg):
        try:
            value = Path(arg).resolve(strict=True)
        except FileNotFoundError as file_not_found_error:
            raise self.exception() from file_not_found_error
        return value

    def exception(self):
        return argparse.ArgumentTypeError('Must be a existing path')

class StrictFilePath:
    def __call__(self, arg):
        try:
            value = Path(arg).resolve(strict=True)
        except FileNotFoundError as file_not_found_error:
            raise self.exception() from file_not_found_error
        if not value.is_file():
            raise self.exception()
        return value

    def exception(self):
        return argparse.ArgumentTypeError('Must be a existing file')

def command_line_runner():

    # create the top-level parser
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "init" command
    parser_init = subparsers.add_parser(
        'init',
        aliases='i',
        help='init a directory for all repositories of problems by adding a compile_args.yml'
    )
    # do not set default for position arguments
    parser_init.add_argument('dir_path', type=Path)
    parser_init.set_defaults(func=init)

    # create the parser for the "new" command
    parser_init = subparsers.add_parser(
        'new',
        aliases='n',
        help='new a single problem by adding a config.yml'
    )
    # do not set default for position arguments
    parser_init.add_argument('dir_path', type=Path)
    parser_init.set_defaults(func=new)

    # create the parser for the "submit" command ...
    parser_submit = subparsers.add_parser(
        'submit',
        aliases='s',
        help='submit and judge the code'
    )
    parser_submit.add_argument('code', type=StrictFilePath())
    parser_submit.set_defaults(func=submit)

    # args = parser.parse_args(namespace=argparse.Namespace())
    args = parser.parse_args()

    # manual print help by this when there is no argument.
    # see https://bugs.python.org/issue9253
    #     https://bugs.python.org/issue16308
    # and parser.set_defaults(func=parser.print_help) failed.
    # Though this below look quite manual compared to the usual way of using argparse.
    if len(args.__dict__) <= 1:
        parser.print_help()
        parser.exit()

    args.func(args)

if __name__ == '__main__':
    command_line_runner()

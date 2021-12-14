import argparse
import pkg_resources
import sys
import subprocess
import os
from pathlib import Path

import yaml
import click
from git import Repo


__version = '0.0.1'


def is_problem_dir(dir_path):
    return (dir_path / 'info.yml').is_file() \
       and is_repository_dir(dir_path.parent)
def is_repository_dir(dir_path):
    return (dir_path / '.git').is_dir() \
       and is_all_repositories_dir(dir_path.parent)
def is_all_repositories_dir(dir_path):
    return (dir_path / 'config.yml').is_file()

# dir of a single problem (a directory with info.yml)
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

# dir of all the repositories (a directory with config.yml)
def all_repositories_dir():
    cwd = Path.cwd()
    if is_problem_dir(cwd):
        return cwd.parents[2]
    elif is_repository_dir(cwd):
        return cwd.parent
    elif is_all_repositories_dir(cwd):
        return cwd
    else:
        return False

def copy_data(file_name, dir_path):
    data = pkg_resources.resource_string(__name__, file_name)
    with open(dir_path / file_name, 'rt') as target_file:
        target_file.write(data)

# init a single problem by adding a info.yml
# init a repository with git
# init a directory of all the repositories by adding a config.yml
def init(args):
    if is_repository_dir(args.dir_path.parent):
        copy_data('info.yml', args.dir_path)
    elif is_all_repositories_dir(args.dir_path.parent):
        repo = Repo.init(args.dir_path + '/.git/', bare=True)
    # else:
    #     copy_data('config.yml', args.dir_path)

# TODO: unknown platform error
# TODO: open multiple files at the same time
# open a file with default software
def open(args):
    except_ext_map = ['tex', 'pdf', 'doc', 'docx']
    if args.file_path.suffix not in except_ext_map:
        click.edit(filename=str(args.path))
    else:
        if sys.platform in ('linux', 'linux2'):
            subprocess.call(["xdg-open", args.path])
        elif sys.platform in ('win32', 'win64'):
            os.startfile(args.path)
        elif sys.platform == 'darwin':
            subprocess.call(["open", args.path])
        else:
            raise UnknownPlatformError

# find and open description doc of a problem
def open_doc(dir_path):
    extlist = ['md', 'txt', 'tex', 'pdf', 'rst', 'doc', 'docx']
    for ext in extlist:
        if Path(dir_path / (str(dir_path.name) + ext)).is_file():
            open(dir_path / (str(dir_path.name) + ext))
            return True
    return False

# TODO: add "ext" in config.yml
def do(args):
    open_doc(args.path.parent)
    if args.path.is_file():
        open(args.path)
    elif args.path.is_dir():
        new_count = len(list(args.path.glob('*.' + args.ext))) + 1
        open(str(args.path) + str(args.path.name) + '_' + str(count) + args.ext)


class StrictPath:
    def __call__(self, arg):
        try:
            value = Path(arg).expanduser().resolve(strict=True)
        except FileNotFoundError as file_not_found_error:
            raise self.exception() from file_not_found_error
        return value

    def exception(self):
        return argparse.ArgumentTypeError('Must be a existing path')

class StrictDirPath:
    def __call__(self, arg):
        try:
            value = Path(arg).expanduser().resolve(strict=True)
        except FileNotFoundError as file_not_found_error:
            raise self.exception from file_not_found_error
        if not value.is_dir():
            raise self.exception()
        return value

    def exception(self):
        return argparse.ArgumentTypeError('Must be a existing directory')

# create the top-level parser
parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "init" command
parser_init = subparsers.add_parser(
    'init',
    aliases='i',
    help='init a problem, a repository, or the directory of all repositories'
)
# do not set default for position arguments
parser_init.add_argument('dir_path', type=Path)
parser_init.set_defaults(func=init)

# create the parser for the "open" command
parser_open = subparsers.add_parser(
    'open',
    aliases='o',
    help='open a file or a directory'
)
parser_open.add_argument('path', type=StrictPath())
parser_open.set_defaults(func=open)

# create the parser for the "do" command ...
parser_do = subparsers.add_parser(
    'do',
    aliases='d',
    help='open the description of a problem and open the source code'
)
parser_do.add_argument('path', type=StrictPath())
parser_do.add_argument('ext', type=str)
parser_do.set_defaults(func=do)

args = parser.parse_args(namespace=argparse.Namespace(dir_path=Path.cwd(), path=Path.cwd()))

# manual print help by this when there is no argument.
# see https://bugs.python.org/issue9253
#     https://bugs.python.org/issue16308
# and parser.set_defaults(func=parser.print_help) failed.
# Though this below look quite manual compared to the usual way of using argparse.
if len(args.__dict__) <= 1:
    parser.print_help()
    parser.exit()

args.func(args)


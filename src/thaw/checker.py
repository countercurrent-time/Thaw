import argparse
import subprocess
import os
import sys
import shlex
from pathlib import Path
# import re

import yaml

from thaw import problem_dir, repository_dir, all_repositories_dir
from thaw import parse_yaml
from thaw import StrictPath, StrictFilePath

# get command by option from compile_args.yml
# "run" option refers to execute the program directly
def get_command(code, option):
    try:
        command = parse_yaml(all_repositories_dir() / 'complie_args.yml')[code.suffix][option]
        return shlex.split(command.replace('%s.*', code).replace('%s', code.stem))
    except KeyError as key_error:
        if option == 'run':
            return [code.stem]
        raise argparse.ArgumentTypeError('nonexistent option') from key_error

# run a command by subprocess.run and catch the exception
def execute(command, time=None, memory=None, stdin=None, stdout=None, stderr=None):
    try:
        return subprocess.run(command, check=True, timeout=time, stdin=stdin, stdout=stdout, stderr=stderr)
    except TimeoutExpired as timeout_expired:
        raise TimeoutExpired(_err('Time Limit Exceeded')) from timeout_expired
    except CalledProcessError as called_process_error:
        raise CalledProcessError(_err('Runtime Error')) from called_process_error

# specific form of execute() for compilation
def compile(code, option='default', stdout=None, stderr=None):
    try:
        return execute(get_command(code, option), time=10, stdout=stdout, stderr=stderr)
    except:
        sys.stderr.write(' '.join(command) + ': Compile Error')
        raise

# specific form of execute() for data generator
def generate(gen, seed, stdin=None, stdout=None, stderr=None):
    try:
        return execute(get_command(gen, 'run').append(seed), stdin=stdin, stdout=stdout, stderr=stderr)
    except:
        sys.stderr.write(' '.join(command) + ': Generator Program Error')
        raise

# specific form of execute() for standard code
def execute_std(std, time=None, memory=None, stdin=None, stdout=None, stderr=None):
    try:
        return execute(get_command(std, 'run'), time=time, space=space, stdin=stdin, stdout=stdout, stderr=stderr)
    except:
        sys.stderr.write(' '.join(command) + ': Standard Program Error')
        raise

# specific form of execute() for user's code
def execute_code(code, time=None, memory=None, stdin=None, stdout=None, stderr=None):
    try:
        return execute(get_command(code, 'run'), time=time, memory, stdin=stdin, stdout=stdout, stderr=stderr)
    except:
        raise

# split stdout and stderr of a subprocess
def parse_output(process):
    if process.stderr != None:
        sys.stderr.write(' '.join(process.args) + ':')
        sys.stderr.write(process.stderr)
    return process.stdout

# ignore space at the end of line and newline at the end of file
def ignore_final_blank(data):
    return data.rstrip().replace('\s\r\n', '').replace('\s\n', '').replace('\s\r', '')

# ignore all of the blank
def ignore_all_blank(data):
    return data.replace('\s', '')

# diff answer and output
def normal_diff(ans, out):
    if ignore_final_blank(ans) == ignore_final_blank(out):
        return 'Accepted'
    else:
        return 'Wrong Answer'

# diff answer and output but can also show Presentation Error
def normal_diff_with_pe(ans, out):
    if ignore_final_blank(ans) == ignore_final_blank(out):
        return 'Accepted'
    elif ignore_all_blank(ans) == ignore_all_blank(out):
        return 'Presentation Error'
    else:
        return 'Wrong Answer'

def delete_executable_file():
    if args.no_delete == False:
        if code.suffix != '':
            code.stem.unlink()
        if gen.suffix != '':
            gen.stem.unlink()
        if std.suffix != '':
            std.stem.unlink()

# judge once for traditional problems
def tradtional(
    code=args.code,
    gen=args.gen,
    std=args.std,
    time=args.time,
    memory=args.memory,
    seed=args.seed,
    option=args.option
):
    try:
        compile(code, option)
        compile(gen)
        compile(std)

        data = parse_output(gen_execute(gen, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        ans = parse_output(execute_std(std, time=time, stdin=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    except:
        raise
    finally:
        delete_executable_file()

    try:
        out = parse_output(execute_code(code, time=time, stdin=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        return normal_diff(ans, out)
    except TimeoutExpired:
        return 'Time Limit Exceeded'
    except CalledProcessError:
        return 'Runtime Error'
    finally:
        delete_executable_file()

if __name == '__main__':
    pass
else:
    parser = argparse.ArgumentParser()
    parser.add_argument('code', type=StrictFilePath())
    parser.add_argument('--gen', type=StrictFilePath(), default=None)
    parser.add_argument('--std', type=StrictFilePath(), default=None)
    parser.add_argument('--time', type=float, default=None)
    parser.add_argument('--memory', type=float, default=None)
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--option', type=str, default='default')
    parser.add_argument('--no-delete', action='store_true')
    print(args.time)

    args = parser.parse_args()


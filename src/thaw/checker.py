import argparse
import subprocess
import os
import sys
import shlex
from pathlib import Path
# import re
import random

import yaml

from thaw.thaw import _err
from thaw.thaw import problem_dir, repository_dir, all_repositories_dir
from thaw.thaw import parse_yaml
from thaw.thaw import StrictPath, StrictFilePath

# get command by option from compile_args.yml
# "run" option refers to execute the program directly
def get_command(code, option):
    try:
        command = parse_yaml(all_repositories_dir() / 'compile_args.yml')[code.suffix[1:]][option]
        if command != None:
            return shlex.split(command.replace('%s.*', str(code)).replace('%s', str(code.stem)))
        # code that do not neew compiler
        else:
            return []
    except KeyError as key_error:
        # code that do not need interpreter
        if option == 'run':
            return [str(code.parent / code.stem)]
        # code that do not need compiler
        if option == 'default':
            return []
        raise argparse.ArgumentTypeError('nonexistent option') from key_error

# run a command by subprocess.run and catch the exception
def execute(command, time=None, memory=None, stdin=None, input=None, stdout=None, stderr=None):
    if command != []:
        try:
            if stdin == None:
                return subprocess.run(command, check=True, timeout=time, input=input, stdout=stdout, stderr=stderr, text=True)
            else:
                return subprocess.run(command, check=True, timeout=time, stdin=stdin, stdout=stdout, stderr=stderr, text=True)
        except subprocess.TimeoutExpired as timeout_expired:
            raise subprocess.TimeoutExpired(_err('Time Limit Exceeded')) from timeout_expired
        except subprocess.CalledProcessError as called_process_error:
            raise subprocess.CalledProcessError(_err('Runtime Error')) from called_process_error
    else:
        return None

class Judger:

    def __init__(self, time, memory, gen=None, std=None, seed=None, option=None):
        parser.parse_args(namespace=self)

        os.chdir(self.code.parent)

        if gen != None:
            self.gen = StrictFilePath()(gen)
        if std != None:
            self.std = StrictFilePath()(std)
        self.time = time
        self.memory = memory

        if seed != None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 2 ** 63)

        if option != None:
            self.option = option

    # specific form of execute() for compilation
    def compile(self, file, stdout=None, stderr=None):
        command = get_command(file, self.option)
        try:
            return execute(command, time=10, stdout=stdout, stderr=stderr)
        except:
            sys.stderr.write(' '.join(command) + ': Compile Error')
            raise
    
    # specific form of execute() for data generator
    def generate(self, stdin=None, stdout=None, stderr=None):
        command = get_command(self.gen, 'run')
        command.append(str(self.seed))
        try:
            return execute(command, stdin=stdin, stdout=stdout, stderr=stderr)
        except:
            sys.stderr.write(' '.join(command) + ': Generator Program Error')
            raise

    # specific form of execute() for standard code
    def execute_std(self, stdin=None, input=None, stdout=None, stderr=None):
        command = get_command(self.std, 'run')
        try:
            return execute(command, time=self.time, memory=self.memory, stdin=stdin, input=input, stdout=stdout, stderr=stderr)
        except:
            sys.stderr.write(' '.join(command) + ': Standard Program Error')
            raise

    # specific form of execute() for user's code
    def execute_code(self, stdin=None, input=None, stdout=None, stderr=None):
        command = get_command(self.code, 'run')
        try:
            return execute(command, time=self.time, memory=self.memory, stdin=stdin, input=input, stdout=stdout, stderr=stderr)
        except:
            sys.stderr.write(' '.join(command) + ': stderr of code of user')
            raise

    # split stdout and stderr of a subprocess
    def parse_output(process):
        if process.stderr != '':
            sys.stderr.write(' '.join(process.args) + ':')
            sys.stderr.write(process.stderr)
        return process.stdout
    
    # ignore space at the end of line and newline at the end of file
    def __ignore_final_blank(data):
        return data.rstrip().replace('\s\r\n', '').replace('\s\n', '').replace('\s\r', '')

    # ignore all of the blank
    def __ignore_all_blank(data):
        return data.replace('\s', '')

    # diff answer and output
    def normal_diff(ans, out):
        if Judger.__ignore_final_blank(ans) == Judger.__ignore_final_blank(out):
            return 'Accepted'
        else:
            return 'Wrong Answer'

    # diff answer and output but can also show Presentation Error
    def normal_diff_with_pe(ans, out):
        if Judger.__ignore_final_blank(ans) == Judger.__ignore_final_blank(out):
            return 'Accepted'
        elif Judger.__ignore_all_blank(ans) == Judger.__ignore_all_blank(out):
            return 'Presentation Error'
        else:
            return 'Wrong Answer'

    def delete_executable_file(self):
        if args.no_delete == False:
            # compatible with python 3.7
            if self.code.suffix != '' and Path(self.code.stem).is_file():
                Path(self.code.stem).unlink()
            if self.gen != None and self.gen.suffix != '' and Path(self.gen.stem).is_file():
                Path(self.gen.stem).unlink()
            if self.std != None and self.std.suffix != '' and Path(self.std.stem).is_file():
                Path(self.std.stem).unlink()

    # judge once for traditional problems
    def traditional(self):
        # if user add arguments [--gen] or [--std] to choose specific generator or standard code
        if (args.gen != None and args.gen != self.gen) or (args.std != None and args.std != self.std):
            return None

        try:
            self.compile(self.code, stderr=sys.stderr)
            self.compile(self.gen, stderr=sys.stderr)
            self.compile(self.std, stderr=sys.stderr)

            data = Judger.parse_output(self.generate(stdout=subprocess.PIPE, stderr=subprocess.PIPE))
            ans = Judger.parse_output(self.execute_std(input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        except:
            raise

        try:
            out = Judger.parse_output(self.execute_code(input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
            self.delete_executable_file()
            return Judger.normal_diff_with_pe(ans, out)
        except subprocess.TimeoutExpired:
            self.delete_executable_file()
            return 'Time Limit Exceeded'
        except subprocess.CalledProcessError:
            self.delete_executable_file()
            return 'Runtime Error'
    
    def output_only(self):
        if args.std != None and args.std != self.std:
            return None

        try:
            self.compile(self.code, stderr=sys.stderr)
            self.compile(self.std, stderr=sys.stderr)

            ans = Judger.parse_output(self.execute_std(stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        except:
            raise

        try:
            out = Judger.parse_output(self.execute_code(stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
            self.delete_executable_file()
            return Judger.normal_diff_with_pe(ans, out)
        except subprocess.TimeoutExpired:
            self.delete_executable_file()
            return 'Time Limit Exceeded'
        except subprocess.CalledProcessError:
            self.delete_executable_file()
            return 'Runtime Error'

if __name__ == '__main__':
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

    args = parser.parse_args()


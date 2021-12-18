#def is_problem_dir(dir_path):
    return (dir_path / 'info.yml').is_file() \
       and is_repository_dir(dir_path.parent)
def is_repository_dir(dir_path):
    return (dir_path / '.git').is_dir() \
       and is_all_repositories_dir(dir_path.parent)
def is_all_repositories_dir(dir_path):
    return (dir_path / 'compile_args.yml').is_file()

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
 TODO: find a package in python to replace "which"
def complie(args):
    with open(all_repositories_dir() / 'complie_args.yml', 'r') as file:
        for command in yaml.load(file)[args.code.suffix][args.option]:
            if sys.platform in ('linux', 'linux2') \
                    and os.system('which ' + command.spilt(' ')[0]):
                compile_by_command(command)
            elif sys.platform in ('win32', 'win64') \
                    and os.system('where ' + command.spilt(' ')[0]):
                compile_by_command(command)

def compile_by_command(command):
    command = command.replace('%s.*', )
    try:
        subprocess.run(command, check=True, timeout=10, output=sys.stdout, stderr=sys.stderr)
    except TimeoutExpired as timeout_expired:
        raise TimeoutExpired(_err('compile timeout')) from timeout_expired
    except CalledProcessError as called_process_error:
        raise CalledProcessError(_err('compile error'))

def execute(program, input, output):
    interpreters_dict = {
        'py': 'python',
        'sh': 'bash',
    }
    if code.suffix in interpreters_dict:
        subprocess.run(interpreters_dict[code.suffix] + ' ' + str(code), checkout=True, timeout=1)
    else:
        subprocess.run(str(code), checkout=True, timeout=1)


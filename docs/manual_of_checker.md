# Example

See [sampleproblem](https://github.com/countercurrent-time/sampleproblem).

# Initialization

Use `from thaw.checker import Judger` in python3, it will initiate automatically.

If you are only a common problem writter, you could only read about [traditional](#traditional) and [output_only](#output_only). But if you want try other forms of problems, you would read about and use most of the APIs.

# get_command

Get command by option from `compile_args.yml`.

"run" option refers to execute the program directly.

# execute

Execute a command by `subprocess.run` and catch the exception.

# Judger

## init

Brief introduction for arguments:

- gen: path to data generator
- std: path to standard code
- time: time limit (in seconds)
- memory: memory limit (in MB) (insignificant yet)
- seed: random seed that will be delivered to data generator in command line arguments.
- option: compilation option (see [The directory of all the repositories](./manual.md#The+directory+of+all+the+repositories))

## compile, generate, execute-std, execute-code

Specific form of `execute()` for compilation, executing generator, standard program, and code of user.

You can set `stdin, input, stdout, stderr` (in `compile` you could not set `input` or `stdin`) by arguments.

Note: Set `input` when using string as input data, otherwise set `stdin`.

## parse_output

Output `stderr` of a process to screen and return its `stdout`. Use it with `subprocess.PIPE`.

## normal_diff

Diff two pieces of data and return `"Accepted"` or `"Wrong Answer"`. Ignore space at the end of line and newline at the end of file.

## normal_diff_with_pe

Like normal_diff, but return '"Presentation Error"' when the two pieces of data are the same but some blanks append in wrong places.
## traditional

Judge once for traditional problems.

## output_only

Judge once for output-only problems.


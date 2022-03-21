A directory of a single problems must have:

- One `config.yml` (add it by `thaw init` and fill in the information)
- One `checker.py`.
- At least one `std.py` or other kinds of standard code.
- At least one `gen.py` or other kinds of data generator (except output-only problems).
- At least one description file, like `name_of_the_problem.zh-CN.md`(or in other languages).

The `checker.py` could use the API by `import thaw.checker`.

# Config

# Checker

# Standard program

# Generator

If you use python, notice that although `range()` is a left closed and right open range, `random.randint` can get the two end points.

# Description of the problem

Reference:

[Codeforces notes to the author](https://docs.google.com/document/d/e/2PACX-1vRhazTXxSdj7JEIC7dp-nOWcUFiY8bXi9lLju-k6vVMKf4IiBmweJoOAMI-ZEZxatXF08I9wMOQpMqC/pub)

[OI wiki 出题](https://oi-wiki.org/contest/problemsetting/#_9)

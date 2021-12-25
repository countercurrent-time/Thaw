A directory of a single problems must have:

- One `config.yml` (add it by `thaw init` and fill in the information)
- One `checker.py`.
- At least one `std.py` or other kinds of standard code.
- At least one `gen.py` or other kinds of data generator.
- At least one description file, like `name_of_the_problem.zh-CN.md`(or in other languages).

The `checker.py` should use the API by `import thaw.checker`.


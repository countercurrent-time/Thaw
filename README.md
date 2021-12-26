# Thaw

[中文](./README.zh-CN.md) | [English](./README.md)

Thaw is an off-line judger supporting distributed problem repositories. Everyone can use Thaw release problems with license on GitHub or other open sourse repositories, get problems locally and judge programs automatically.

We request people who write problems add licenses to their problems or clear copyright notice so that problems can be shared easier, and data generator and solution as well, which can support generalization test and help improve the problems.

By making it off-line, distributed and based on GitHub, situations in which a few administrators examine a large number of problems can be prevented. The nice atmosphere on GitHub can also make quanlity of discussion higher.

We also hope to improve traditional methods of judging. Making it off-line helps avoid creating motivation of cheating, and we hope people do not exceedingly pursue the optimization of the program, but concentrate on things like the readability of code. We will support judging with less strict limit of time and memory, and estimating the polynomial time complexity of a program.

We will make it simple to configure and highly hackable too.

## Installation

Package will be created and be released on pip and GitHub after enough improvement and tests on 0.0.1.

## Manual

See `./docs/manual.md`.

Also See [sampleproblem](https://github.com/countercurrent-time/sampleproblem) about how to write a problem with Thaw for example.

## Usage

Sorry for the project being incompleted. But it will be completed as quick as possible.

Below are expected result.

Create a problem:

```bash
thaw init .
git init sampleproblem
cd sampleproblem
thaw init hello_world
cd hello_world
vim -p hello_world.zh-CN.md hello_world.en-US.md std.cpp std.py checker.py
```

Solve a problem:

```bash
vim hello_world.cpp
thaw submit hello_world.cpp
```

Release a problem:

```bash
git add .
git commit -m "add hello_world"
git remote add origin https://github.com/username/sampleproblem
git push origin master
```

Download a problem:

```bash
git clone https://github.com/username/sampleproblem
```

## How to contribute

Welcome to join us! You can improve Thaw by send an Issue or a Pull Request.

Or create a GitHub repository to release your problem [according to the format](docs/release_your_problems.md), and create open and shared atmosphere of algorithm contest with us. You can add the url of your repository to [repositories.dat](./src/thaw/repositories.dat) to make it easy for others to get your problems and spread your problems.

We will create a Gitter group when more people join.

## Contributors

Thank [peers who improve Thaw together and share problems](https://github.com/countercurrent-time/Thaw/graphs/contributors)！

## License

[AGPL](LICENSE)


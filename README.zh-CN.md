# Thaw

[中文](./README.zh-CN.md) | [English](./README.md)

Thaw 是一个支持分布式题库的离线评测系统，大家可以使用 Thaw 在 GitHub 或其它开放源代码仓库上自由地发布带有许可证的题目，同时在本地获取题目并进行自动评测。

我们要求命题者为题目附带许可证或清晰的版权声明以使得题目更容易被共享，并要求命题者提供数据生成器和题解，在支持更一般化的测试的同时，能使题目被更好地改进。

离线、分布式和基于 GitHub 使少数管理员审核大量题目的困扰和所带来的问题不会出现，GitHub 良好的社区氛围也会促使讨论具有高质量。

我们希望改进传统评测方式的缺点。在离线化避免带来抄袭动机的同时，我们希望大家不要过度追求程序的时空优化，而是重新集中在代码的可读性等要素上。我们允许不严格的时空限制，并支持通过统计学大致估计程序的多项式的时空复杂度。

我们还会努力实现配置简单和高度自定义。

## 安装

在 0.0.1 版本经过足够的完善和测试后，发行版会被创建，并被发布到 pip 和 GitHub 上。

## 使用说明

参考 `./docs/manual.md`。

还可以参考 [sampleproblem](https://github.com/countercurrent-time/sampleproblem) 作为使用 Thaw 编写题目的示例。

## 示例

创建一个题目：

```bash
thaw init .
git init sampleproblem
cd sampleproblem
thaw new hello_world
cd hello_world
vim -p hello_world.zh-CN.md hello_world.en-US.md std.cpp std.py checker.py
```

解题：

```bash
vim hello_world.cpp
thaw submit hello_world.cpp
```

发布题目（不包含解题代码）：

```bash
git add .
git commit -m "add hello_world"
git remote add origin https://github.com/username/sampleproblem
git push origin master
```

下载题目：

```bash
git clone https://github.com/username/sampleproblem
```

## 如何贡献

非常欢迎你的加入！你可以通过提一个 Issue 或者提交一个 Pull Request 来改进 Thaw。

或者[按照格式](docs/release_your_problems.md)建立 GitHub 仓库以发布你的题目，并和我们一起创造开放共享的算法竞赛氛围。通过将你的仓库链接添加到 [repositories.dat](./src/thaw/repositories.dat)，可以方便其他人获取你的题目，并宣传你的题目。

当参与者增多时，我们会建立 Gitter 群组。

## 贡献者

非常感谢[一起改进 Thaw 的小伙伴们和一起共享题目的小伙伴们](https://github.com/countercurrent-time/Thaw/graphs/contributors)！

## 使用许可

[AGPL](LICENSE)


# IPython memory magic commands

[![PyPI](https://img.shields.io/pypi/v/ipython-memory-magics?color=brightgreen)](https://pypi.org/project/ipython-memory-magics/)

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://wemake-python-styleguide.readthedocs.io/en/latest/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

Simple tool to trace memory usage of a Python statement or expression execution.

Memory equivalent of IPython
built-in [time magics](https://github.com/ipython/ipython/blob/66aeb3fc55c8ac04242e566172af5de5cc6fe71e/IPython/core/magics/execution.py#L1193).

Existing tools like [memory-profiler](https://github.com/pythonprofilers/memory_profiler)
or [ipython-memory-usage](https://github.com/ianozsvald/ipython_memory_usage) mainly use psutil package to measure
memory usage, which may give inaccurate results. This package
uses [tracemalloc](https://docs.python.org/3/library/tracemalloc.html) module to trace Python memory allocations.
Memory-profiler provides tracemalloc backend, but it does not allow to use it for magic commands. This packages offers
line `%memory` and cell `%%memory` magic commands, which were intended to complement the `%time` and `%%time` magic
commands.

# Installation

Install from pip:

```
pip install ipython-memory-magics
```

Or install directly from github:

```
pip install git+https://github.com/rusmux/ipython-memory-magics.git
```

After the installation load the extension via:

```
%load_ext memory_magics
```

To activate it whenever you start IPython, edit the configuration file for your IPython
profile `~/.ipython/profile_default/ipython_config.py`. Register the extension like this:

```
c.InteractiveShellApp.extensions = [
    'memory_magics',
]
```

If the file does not already exist, run `ipython profile create` in a terminal.

# Usage

Use `%memory [options] statement` to measure `statement`'s memory consumption:

```python
% memory - q
list(range(10 ** 6))
```

The output in the format `current / peak` will follow:

```
RAM usage: line: 34.33 MiB / 34.33 MiB
```

Here `-q` is the `quiet` flag set to suppress the output. You can use other options to get data on the notebook and
jupyter memory usage, or to print the statistics in a table. For example, you can use `-n` or `--notebook` flag to get
the information about the notebook current memory consumption:

```python
% memory - n
```

```
RAM usage: notebook: 101.41 MiB
```

In the same way, `-j` or `--jupyter` flag will give you the information about the total Jupyter memory usage.

Put `%%memory [options]` on top of a cell to measure its memory consumption:

```python
In[1]: % % memory - n - j - t
sum(list(range(10 ** 6)))
```

This will print:

```
RAM usage |   current   |     peak     |
----------------------------------------
 cell     | 2.62 KiB    | 34.33 MiB    |
 notebook | 123.08 MiB  | 155.53 MiB   |
 jupyter  | 170.19 MiB  | 202.55 MiB   |

Out [1]: 499999500000
```

# Options

Five options are available in full and short versions:

`-n <notebook>`: If present, show current notebook memory usage

`-j <jupyter>`: If present, show current jupyter memory usage

`-i <interval>`: Interval in milliseconds for updating memory usage information

`-t <table>`: If present, print statistics in a table

`-q <quiet>`: If present, do not return the output

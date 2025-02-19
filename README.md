# python-importlens

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![python](https://img.shields.io/badge/Python-3.10--3.12-3776AB?logo=python&logoColor=white)](https://www.python.org)

The `inspect_imports` function in [this file](./src/importlens/importlens.py) is used to get all import statements in the caller's frame.

If more than `max_obj` objects are imported from a module, they will be displayed as a wildcard, i.e., `from ... import *`. Increase the value of `max_obj` if needed.

The original intention to write this function was to verify the imports in LeetCode's Python3 environment.
For example, in a LeetCode editor, copy & paste `inspect_imports` function then call it by `print('\n'.join(inspect_imports()))` to print the results to stdout.
Also works for HackerRank.

## Installation

Install this module:

```sh
# Install from GitHub
python3 -m pip install git+https://github.com/lydiazly/python-importlens.git
# Or install from local clone in editable/develop mode
git clone https://github.com/lydiazly/python-importlens.git
cd python-importlens
python3 -m pip install -e .
```

To uninstall:

```sh
python3 -m pip uninstall importlens
```

## Usage

Example:

```sh
python3 ./examples/example_usage.py
```

## Testing

Install requirements:

```sh
python3 -m pip install -r requirements.txt
```

```sh
pytest tests
```

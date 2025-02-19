# -*- coding: utf-8 -*-
# tests/test_inspect_imports.py
import pytest
import warnings
from src.importlens import inspect_imports, verify_imports


default_ignore_list = ['@py_builtins', 'pytest', '_pytest', 'warnings', 'tests', 'verify_imports']
module_not_found_msg = "Module not found (probably not installed)"
verbose = False

#------------------------------------------------------------------------------|
# import_str, max_obj, ignore, expected (set None to use the default argument values)
test_cases_regular_imports = [
    ("from math import floor, sqrt, isnan", None, None,
     "from math import floor, sqrt, isnan"),
    ("from math import floor, inf, sqrt, isnan", None, None,
     "from math import floor, sqrt, isnan"),
    ("from math import floor, inf, sqrt, isnan, log", None, None,
     "from math import *"),
    ("from operator import add, mul, eq, countOf", None, None,
     "from operator import *"),
    ("import urllib", None, None,
     "import urllib"),
    ("from json.decoder import JSONDecoder, JSONDecodeError", None, None,
     "from json.decoder import JSONDecoder, JSONDecodeError"),
    ("from json.encoder import JSONEncoder", None, None,
     "from json.encoder import JSONEncoder"),
    ("from json.encoder import re", None, None,
     "import re"),
]

test_cases_regular_imports_need_install = [
    ("import requests", None, None,
     "import requests"),
    ("import numpy as np\nimport numpy.random as random\nfrom numpy.random import rand", None, None,
     "import numpy as np\nimport numpy.random as random\nfrom numpy.random import rand"),
    ("from numpy import random", None, None,
     "import numpy.random as random"),
    ("import matplotlib\nfrom matplotlib import cm\nimport matplotlib.pyplot as plt", None, None,
     "import matplotlib\nimport matplotlib.cm as cm\nimport matplotlib.pyplot as plt"),
    ("from scipy import stats", None, None,
     "import scipy.stats as stats"),
    ("import pandas as pd", None, None,
     "import pandas as pd"),
]

test_cases_wildcard_imports = [
    ("from os import *", None, None,
     "import posixpath as path\nfrom builtins import OSError as error\nfrom os import *\nfrom posix import *"),
    # ("from sys import *", None, None,
    #  "import sys.monitoring as monitoring\nfrom sys import *"),  # where "import sys.monitoring as monitoring" is invalid and only appears in python3.12
    ("from datetime import *", None, None,
     "from datetime import *"),
    ("from time import *", None, None,
     "from time import *"),
    ("from math import *", None, None,
     "from math import *"),
    ("from random import *", None, None,
     "from random import *"),
    ("from json import *", None, None,
     "from json import *\nfrom json.decoder import JSONDecoder, JSONDecodeError\nfrom json.encoder import JSONEncoder"),
    ("from csv import *", None, None,
     "from csv import *"),
    ("from collections import *", None, None,
     "from collections import *"),
    ("from re import *", None, None,
     "from re import *"),
    # ("from socket import *", None, None,
    #  "from socket import *"),
    ("from pathlib import *", None, None,
     "from pathlib import *"),
    ("from json.decoder import *", None, None,
     "from json.decoder import JSONDecoder, JSONDecodeError"),
]

test_cases_max_obj = [
    ("from math import floor, inf, sqrt, isnan", 2, None,
     "from math import *"),
    ("from datetime import *", 6, None,
     "from datetime import date, datetime, time, timedelta, timezone, tzinfo"),
]

test_cases_ignore = [
    ("from math import floor, inf, sqrt, isnan", None, ['sqrt',],
     "from math import floor, isnan"),
    ("from operator import add", None, ['add',], ""),
    ("from operator import add", None, ['operator.add',], ""),
    ("from operator import add as addition", None, ['addition',], ""),
    ("import numpy as np", None, ['numpy',], ""),
    ("import numpy as np", None, ['np',], ""),
    ("import numpy.random as random", None, ['numpy',], ""),
    ("import numpy.random as random", None, ['numpy.random',], ""),
    ("import numpy.random as random", None, ['random',], ""),
    ("from numpy import random", None, ['random',], ""),
    ("from numpy import random", None, ['numpy.random',], ""),
    ("import matplotlib.pyplot as plt", None, ['matplotlib',], ""),
    ("import matplotlib.pyplot as plt", None, ['matplotlib.pyplot',], ""),
    ("import matplotlib.pyplot as plt", None, ['pyplot',], ""),
    ("import matplotlib.pyplot as plt", None, ['plt',], ""),
]

test_cases_max_obj_ignore = [
    ("from math import floor, inf, sqrt, isnan", 1, ['sqrt',],
     "from math import *"),
    ("from datetime import *", 4, ['timedelta',],
     "from datetime import *"),
]

@pytest.mark.parametrize(
    "import_str, max_obj, ignore, expected",  # set None to skip the argument
    [
        *[pytest.param(*values, id="test_cases_regular_imports") for values in test_cases_regular_imports],
        *[pytest.param(*values, id="test_cases_regular_imports_need_install") for values in test_cases_regular_imports_need_install],  # will skip
        *[pytest.param(*values, id="test_cases_wildcard_imports") for values in test_cases_wildcard_imports],
        *[pytest.param(*values, id="test_cases_max_obj") for values in test_cases_max_obj],
        *[pytest.param(*values, id="test_cases_ignore") for values in test_cases_ignore],
        *[pytest.param(*values, id="test_cases_max_obj_ignore") for values in test_cases_max_obj_ignore],
    ]
)
def test_imports(import_str: str, max_obj: int, ignore: list[str], expected):
    """Tests the import statements returned by `inspect_imports`. No verification."""
    kwargs = {'ignore': default_ignore_list}
    if max_obj is not None:
        kwargs |= {'max_obj': max_obj}
    if ignore is not None:
        kwargs['ignore'] += ignore
    try:
        exec(import_str)
        results = '\n'.join(inspect_imports(**kwargs))
        verbose and print('\n' + '-' * 10 + '\n' + results + '\n' + '-' * 10)
        assert results == expected
    except ModuleNotFoundError:
        pytest.skip(reason=f"{module_not_found_msg}: {import_str}")


#------------------------------------------------------------------------------|
# name1, name2, replaceable
test_cases_module_names_replaceable = [
    ('bisect', '_bisect', True),
    ('csv', '_csv', True),
    ('heapq', '_heapq', True),
    ('operator', '_operator', True),
    ('functools', '_functools', True),
]

test_cases_module_names_irreplaceable = [  # has issues when using the function inspect_imports()
    ('json.encoder', '_json', False),
    ('socket', '_socket', False),
]

@pytest.mark.parametrize(
    "name1, name2, replaceable",
    [
        *[pytest.param(*values, id="test_cases_modules_replaceable") for values in test_cases_module_names_replaceable],
        # *[pytest.param(*values, id="test_cases_modules_irreplaceable") for values in test_cases_module_names_irreplaceable],  # will print warnings
    ]
)
def test_module_names(name1, name2, replaceable):
    """ Tests module names.

    If an object imported from module 1 is shown as from module 2,
    verify whether the imports from module 2 can be replaced by those from module 1.
    """
    import inspect

    if not replaceable:
        warnings.warn(f"\n**Avoid wildcard import `from {name1} import *` in practice.**")

    import_str = f"from {name1} import *"
    try:
        exec(import_str)
    except ModuleNotFoundError:
        pytest.skip(reason=f"{module_not_found_msg}: {import_str}")

    locals_dict = inspect.currentframe().f_locals.copy()
    flag = True
    for name, obj in locals_dict.items():
        if name.startswith('__'):
            continue

        module = inspect.getmodule(obj)
        if module:
            try:
                obj_name = obj.__name__
            except AttributeError:
                continue
            module_name = module.__name__

            # Skip some modules
            if module_name.startswith('__') or module_name in [__name__, 'inspect', name1]:
                continue

            """
            1. If 'from {name2} import {obj_name} as {name}' can be replaced by
               'from {name1} import {obj_name} as {name}' or 'from {name1} import {name}',
               mark the case as replaceable and can be added to the mapping dict in `inspect_imports`.
            2. If 'from {name1} import {obj_name} as {name}' or 'from {name1} import {name}' is the same as
               'from {module_name} import {obj_name} as {name}', but '{module_name}' is different from '{name2}',
               print a warning message (use `pytest -s` to see). However, it won't affect the replacement.
            """
            import_str_tmp1_1 = f"from {name1} import {name} as {name}_1_1"  # from module 1
            import_str_tmp1_2 = f"from {name1} import {obj_name} as {name}_1_2"  # from module 1
            import_str_tmp2 = f"from {module_name} import {obj_name} as {name}_2"  # from the module returned by `inspect.getmodule`

            # Import the object from module 1
            verbose and print(f"\nChecking: {import_str_tmp1_1}")
            exec(import_str_tmp1_1)  # must work
            if obj_name != name:  # '{obj_name}' must refer to an object, and '{name}' may be an alias of '{obj_name}'
                try:
                    verbose and print(f"Checking: {import_str_tmp1_2}")
                    exec(import_str_tmp1_2)
                    locals_dict_tmp = inspect.currentframe().f_locals.copy()
                    if locals_dict_tmp[f"{name}_1_1"] is not locals_dict_tmp[f"{name}_1_2"]:
                        # Now we know that '{name}' is not an alias of '{obj_name}'.
                        print(f"\nWARNING: Name '{name}' from '{name1} is different from '{obj_name}' from {name1}.")
                        # In the case, whenever 'from {name2} import {obj_name} as {name}' is valid,
                        # it can't be replaced by 'from {name1} import {obj_name} as {name}'.
                        flag = False
                        continue
                except ImportError:
                    print(f"\nWARNING: Name '{name}' is in '{name1}' but the object name '{obj_name}' is not in '{name1}'. ")
                    # In the case, whenever 'from {name2} import {obj_name} as {name}' is valid,
                    # it can't be replaced by 'from {name1} import {obj_name} as {name}'.
                    flag = False
                    continue

            # Import the object from module 2
            try:
                verbose and print(f"Checking: {import_str_tmp2}")
                exec(import_str_tmp2)  # try the module returned by `inspect.getmodule`
                if module_name != name2:
                    # In this case, the '{module_name}' we found is the actual module containing '{obj_name}'
                    # and '{name}' could be an alias of '{obj_name}'. Print a warning message.
                    # We see that it's not affecting whether '{name2}' can be replaced by '{name1}'
                    # since the module we found is not '{name2}'.
                    print(f"\nWARNING: Name '{obj_name}' is in '{module_name}' but not '{name2}'.")

                locals_dict_tmp = inspect.currentframe().f_locals.copy()

                # Check that if the names from both modules refer to the same object.
                # If so, in cases where '{name2}' == '{module_name}', the possible returned statement
                # 'from {name2} import {name}' can be replaced by 'from {name1} import {name}' (if '{obj_name}' == '{name}'),
                # or 'from {name2} import {obj_name} as {name}' can be replaced by 'from {name1} import {obj_name} as {name}'
                if locals_dict_tmp[f"{name}_1_1"] is not locals_dict_tmp[f"{name}_2"]:
                    flag = False
                    continue
            except ImportError:
                # If '{obj_name}' is not in '{module_name}', the 'from {name2} import {obj_name} as {name}' is invalid.
                print(f"\nWARNING: Cannot import name '{obj_name}' from '{name2}'.")
                flag = False
                continue
    assert flag == replaceable


#------------------------------------------------------------------------------|
# import_list, timeout, expected
test_cases_verify = [
    (["import os", "import dummy", "from os import dummy"], None, ["import dummy", "from os import dummy"]),
    (["import os",], None, []),
    (["import sys.monitoring as monitoring",], None, ["import sys.monitoring as monitoring",]),
    ([], None, []),
]

test_cases_verify_timeout = [
    (["import os", "import sys"], 0, ["import os", "import sys"]),
]

test_cases_verify_leetcode = [
    (["import bisect",
      "import collections",
      "import copy",
      "import datetime",
      "import functools",
      "import heapq",
      "import io",
      "import itertools",
      "import json",
      "import math",
      "import operator",
      "import random",
      "import re",
      "import statistics",
      "import string",
      "import sys",
      "from bisect import insort_right as insort",
      "from builtins import OSError as EnvironmentError",
      "from builtins import OSError as IOError",
      "from builtins import str as Text",
      "from copy import Error, deepcopy",
      "from json.decoder import JSONDecoder, JSONDecodeError",
      "from json.encoder import JSONEncoder",
      "from string import capwords, Formatter, Template"], None, []),
]

@pytest.mark.parametrize(
    "import_list, timeout, expected",  # set None to skip the argument
    [
        *[pytest.param(*values, id="test_cases_verify") for values in test_cases_verify],
        *[pytest.param(*values, id="test_cases_verify_timeout") for values in test_cases_verify_timeout],
        *[pytest.param(*values, id="test_cases_verify_leetcode") for values in test_cases_verify_leetcode],
    ]
)
def test_verification(import_list: list[str], timeout, expected):
    """Tests the import verification."""
    if timeout is None:
        invalid_list = verify_imports(import_list)
    else:
        with pytest.warns(UserWarning, match="Timed out"):
            invalid_list = verify_imports(import_list, timeout=timeout)
    assert invalid_list == expected

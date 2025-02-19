#!/usr/bin/env python
# -*- coding: utf-8 -*-
# examples/example_usage.py
"""Example to print import statements within the current scope and verify the results."""
import os
import sys
import urllib  # noqa

# Append the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.importlens import inspect_imports, verify_imports


# This function is the immediate caller of `inspect_imports`,
# so only objects in it's frame and the global objects are considered.
def example_func():
    max_obj = 13
    ignore = ['os', 'sys', 'verify_imports']

    try:
        from math import floor, sqrt, isnan  # noqa
        import numpy as np  # noqa
        import numpy.random as random  # noqa (same as `from numpy import random`)
        import matplotlib  # noqa
        from matplotlib import cm  # noqa
        import matplotlib.pyplot as plt  # noqa
        from scipy import stats  # noqa
        import pandas as pd  # noqa
    except ModuleNotFoundError:
        pass

    import_list = inspect_imports(max_obj=max_obj, ignore=ignore)

    # Verify the import statements
    invalid_list = verify_imports(import_list, verbose=True)
    if len(invalid_list) > 0:
        import_list = [s for s in import_list if s.strip() not in invalid_list]
        print("# Invalid statements are removed from the results.")

    if len(import_list) > 0:
        import_str = '\n'.join(import_list)
        if '*' in import_str:
            print(f"# Objects are shown as '*' if more than {max_obj}")
        print(import_str)
    """
    import matplotlib
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import numpy as np
    import numpy.random as random
    import pandas as pd
    import scipy.stats as stats
    import urllib
    from math floor, sqrt, isnan
    """


def main():
    from operator import mul  # noqa (will not be in the results)
    example_func()


###############################################################################|
if __name__ == '__main__':
    main()

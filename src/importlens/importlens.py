# -*- coding: utf-8 -*-
# src/importlens/importlens.py
"""Functions to inspect imported modules in the caller's frame."""


def inspect_imports(max_obj: int = 3, ignore: list[str] = []) -> list[str]:
    """Inspects all imported modules in the immediate caller's frame and reconstructs the statements.

    Args:
        max_obj (int): If more than `max_obj` are imported from a module, they will be represented as a wildcard,
            i.e., `from ... import *`. Defaults to 3. Increase the value if needed.
        ignore (list): Modules or objects, including aliases, to be ignored. Defaults to [].

    Returns:
        list: Import statement strings.

    Examples:
        In a LeetCode editor, copy & paste this function then call it by `print('\\n'.join(inspect_imports()))`.

        In console:
        >>> from importlens import inspect_imports
        >>> print('\\n'.join(inspect_imports()))

    **Limitations:**
    1. Variables of primitive types will be ignored since they will lose their connection to the modules after being imported.
    2. If some objects imported from module A are shown as from module B by `__module__` or `inspect.getmodule`, \
        but are not accessible in module B, then wrong statements might be returned. \
        E.g., 'monitoring' in 'sys' and 'c_make_encoder' in 'json.encoder'.
    """
    # Module names that can be replaced
    # Only a few common ones are listed here. Add more if needed.
    module_mapping = {
        '_bisect': 'bisect',  # verified
        '_csv': 'csv',  # verified
        '_heapq': 'heapq',  # verified
        '_operator': 'operator',  # verified
        '_functools': 'functools',  # verified
    }

    import inspect

    # Get all objects in the caller's frame
    frame=inspect.currentframe().f_back  # `f_back`: the immediate caller's frame (next outer frame)
    globals_dict = frame.f_globals | frame.f_locals

    # Remove local modules
    for module in ['inspect',]:
        globals_dict.pop(module, None)

    imports = {}
    regular_import_str_list = []
    specific_import_str_list = []

    # Check each object
    for name, obj in globals_dict.items():
        if name.startswith('__'):
            continue

        # `inspect.getmodule` returns the module the object is defined in, or None if not found.
        module = inspect.getmodule(obj)

        if module:
            try:
                obj_name = obj.__name__
                module_name = module.__name__
                # print(name, obj_name, module_name)

                # Replace module names
                if module_name in module_mapping:
                    module_name = module_mapping[module_name]

                # Skip exceptions
                if (
                    module_name.startswith('__') or
                    module_name in [__name__,] + ignore or module_name.split('.')[0] in ignore or
                    obj_name in ignore or obj_name.split('.')[-1] in ignore or
                    name in ignore or name.split('.')[-1] in ignore
                ):
                    continue

                # Identify this object
                if inspect.ismodule(obj) and obj_name == module_name:  # this object is the module itself
                    if name == obj_name:  # is not an alias
                        regular_import_str_list.append(f"import {obj_name}")
                    else:  # is an alias
                        regular_import_str_list.append(f"import {obj_name} as {name}")
                else:  # this object is from this module
                    if '.'.join([module_name, obj_name]) in ignore:  # check the name 'module.object'
                        continue
                    if name == obj_name:  # is not an alias
                        if module_name not in imports:
                            imports[module_name] = []
                        imports[module_name].append(name)
                    else:  # is an alias
                        specific_import_str_list.append(f"from {module_name} import {obj_name} as {name}")

            except AttributeError:
                pass

    # Format the specific imports
    for module, names in imports.items():
        if len(names) > max_obj:  # wildcard imports
            specific_import_str_list.append(f"from {module} import *")
        else:
            specific_import_str_list.append(f"from {module} import {', '.join(names)}")

    # Sort (case-insensitive) each list and return a joined list
    return (
        sorted(regular_import_str_list, key=str.casefold) +
        sorted(specific_import_str_list, key=str.casefold)
    )

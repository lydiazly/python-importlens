# -*- coding: utf-8 -*-
# src/importlens/verify.py
"""Functions to verify the reconstructed statements."""
import sys
import subprocess
import warnings


def verify_imports(import_list: list[str], timeout=5, verbose=False) -> list[str]:
    """Verifies the import statements and returns a list of invalid ones."""
    if not import_list:
        return []

    test_program = f"""# Imports a module
for import_str in {import_list}:
    try:
        exec(import_str.strip())
    except (ModuleNotFoundError, ImportError):
        print(import_str.strip())
"""

    invalid_list = []
    try:
        # Run in a new Python process
        verbose and print("Verifying the import statements...")
        result = subprocess.run(
            [sys.executable, "-c", test_program],
            capture_output=True,
            text=True,
            timeout=timeout  # in seconds
        )
        invalid_str = result.stdout.strip()
        if not invalid_str:
            verbose and print("--- All imports are verified ---")
        else:
            invalid_list = [line for line in invalid_str.split('\n')]
            if verbose:
                print("--- These import statements are invalid ---")
                for s in invalid_list:
                    print(f"# {s}")
                verbose and print('-' * 43)
        return invalid_list

    except subprocess.TimeoutExpired:
        warnings.warn(UserWarning(f"Timed out after {timeout} seconds. Verification failed."))
        return import_list

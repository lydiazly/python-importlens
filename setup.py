# setup.py
from setuptools import setup, find_packages

setup(
    name="importlens",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
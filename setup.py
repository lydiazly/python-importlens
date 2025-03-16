#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup.py
from setuptools import setup, find_packages

setup(
    author="lydiazly",
    name="importlens",
    description="Get all import statements in the caller's frame. Originally created for LeetCode's Python3 environment.",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/lydiazly/python-importlens",
    version="0.1.0",
)
#!/usr/bin/env python3

#### META: Title: Package Setup
#### META: Version: 0.1.0-alpha
#### META: PATH: setup.py

from setuptools import setup, find_packages

setup(
    name="wallace",
    version="0.1.0-alpha",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)

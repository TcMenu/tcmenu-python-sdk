#!/usr/bin/env python3
import os
import subprocess
from setuptools import setup, find_packages
from pathlib import Path

this_directory = os.path.abspath(os.path.dirname(__file__))


def read_lines(file_name):
    with open(os.path.join(this_directory, file_name), encoding="utf-8") as file:
        return file.readlines()


install_requirements = list(
    filter(lambda line: not line.startswith("--extra-index-url"), read_lines("requirements.txt"))
)
test_requirements = list(
    filter(lambda line: not line.startswith("--extra-index-url"), read_lines("requirements-test.txt"))
)

APP_VERSION = "0.1.0"

setup(
    name="tcmenu-python",
    version=APP_VERSION,
    author="Lutemi",
    author_email="vladimir.zahradnik@lutemi.com",
    description="A series of domain and serialisation components for the TcMenu library.",
    license="Apache 2.0",
    packages=find_packages(),
    python_requires=">=3.7",
    long_description=open("README.md").read(),
    install_requires=install_requirements,
    tests_require=test_requirements,
    extras_require={"test": test_requirements},
)

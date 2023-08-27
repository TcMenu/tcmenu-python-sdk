#!/usr/bin/env python3
import os

from setuptools import setup, find_packages

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


def read_version():
    with open("tcmenu/__init__.py") as f:
        return next(
            (line.split("=")[1].strip().strip('"').strip("'") for line in f if line.startswith("__version__")), "0.0.0"
        )


setup(
    name="tcmenu-python",
    version=read_version(),
    author="Vladimír Záhradník",
    author_email="vladimir@zahradnik.io",
    description="A series of domain and serialisation components for the TcMenu library.",
    license="Apache 2.0",
    packages=find_packages(),
    python_requires=">=3.7",
    long_description=open("README.md").read(),
    install_requires=install_requirements,
    tests_require=test_requirements,
    extras_require={"test": test_requirements},
)

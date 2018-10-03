#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="block_tracing",
    version='1.0.0',
    author="Rian Hunter",
    author_email="rian@alum.mit.edu",
    description="Protect process memory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rianhunter/block_tracing',
    license="MIT",
    py_modules=["block_tracing"],
)

#!/usr/bin/env python
import imp
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import find_packages, setup

description = "Controlling and emulating NST-style bots"

root = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(root, 'README.md')) as readme:
    long_description = readme.read()

setup(
    name="omnibot",
    version=0.1,
    author="CNRGlab at UWaterloo, NST Lab at TUMunich",
    author_email="tcstewar@uwaterloo.ca, cristian.axenie@tum.de",
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    description=description,
    long_description=long_description,
    requires=[
    ],
)

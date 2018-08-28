#!/usr/bin/env python2

import os
import sys

from setuptools import setup
from setuptools import find_packages

long_description = open(os.path.join(sys.path[0], 'README.md')).read()

setup(
    name='kicad-python',
    version='0.0.2',
    author='Thomas Pointhuber',
    author_email='thomas.pointhuber@gmx.at',
    url='https://github.com/pointhi/kicad-python',
    description="unofficial abstraction layer for the KiCad API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPL3+",

    install_requires=[],
    packages=find_packages('.', exclude=['tests*']),
    test_suite='tests',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2 :: Only',  # not because of our implementation, but because of KiCad
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
    ],
)

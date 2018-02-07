#!/usr/bin/env python2

from setuptools import setup

setup(
    name='kicad',
    version='0.1',
    author='Thomas Pointhuber',
    author_email='thomas.pointhuber@gmx.at',
    url='https://github.com/pointhi/kicad-python',
    description="abstraction layer for the kicad api",
    long_description="""
        The KiCad python interface is a 1:1 representation of the underlying API. Doing scripting on this interface
        is in one side error prone due to changes, and also means we need to handle all that stuff in a C++ way.
        Abstracting this API allows us to write code on a defined and stable codebase in a "pythonic" way.
        """,
    license="GPL3+",

    install_requires=[],
    packages=['kicad'],
    package_data={'': ['gdot.glade']},
    entry_points=dict(gui_scripts=['gdot=gdot.gdot:main']),
    test_suite='tests',

    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
)

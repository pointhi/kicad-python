# kicad-python

Abstraction layer for the KiCad python interface.

Be aware this is in initial development and the interface can change anytime!

Inspired by https://github.com/pierstitus/kicad-python

[![Build Status](https://travis-ci.org/pointhi/kicad-python.svg?branch=master)](https://travis-ci.org/pointhi/kicad-python)
[![Documentation Status](https://readthedocs.org/projects/kicad-python-python/badge/?version=latest)](http://kicad-python-python.readthedocs.io/en/latest/?badge=latest)
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)

## Example usage

```python
from kicad.pcbnew import Board

b = Board.from_file('path/to/file.kicad_pcb')

for module in b.modules:
    print(module)
```

## Run Tests

```bash
./setup.py test
```
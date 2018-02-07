# kicad-python

Abstraction layer for the KiCad python interface.

Be aware this is in initial development and the interface can change anytime!

Inspired by https://github.com/pierstitus/kicad-python

## Example usage

```python
from kicad.pcbnew import Board

b = Board.from_file('path/to/file.kicad_pcb')

for module in b.modules:
    print(module)
```

## Run Tests

```bash
python2 ./setup.py test
```
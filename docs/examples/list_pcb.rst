List PCB Entities
=================

This examples is a reimplementation of the `listPcb.py <https://github.com/KiCad/kicad-source-mirror/blob/master/pcbnew/python/examples/listPcb.py>`_
script found in the official KiCad repository. It basically loads a board and then prints a short representation of all vias, tracks, drawings modules and zones.


.. literalinclude:: ./../../examples/list_pcb.py

This script can now simply be executed from the commandline, and outputs some nice
informations about the board file:

.. code-block:: bash

   $ python ./examples/list_pcb.py ./tests/pcbnew/testproject/testproject.kicad_pcb

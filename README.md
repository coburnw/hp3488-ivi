# hp3488-ivi
HP3488 Switch/Control Unit driver for Python-IVI

A simple but functional driver for interacting with the HP 3488A and 3499A
Switch/Control Unit and their plugins.

The HP 3488A is a modern styled (pre Agilent) (ugly) rack for various
switch modules often used for routing signals between 
devices for product development or test.

This driver is composed of a driver for each plugin and the 3488A rack
itself.  The following plugins are functional:
  * 44470A Ten Channel Differential Mux
  * 44472A Dual Four Channel VHF Mux
  * 44473A 4 X 4 Matrix Switch (planned)

A preliminary 3488A driver has been added which currently only
manages the plugins, but could conceivably implement some sort of
smart routing between plugins in the future.
Very much a work in progress.  

### Requirements
  * developed and tested with Python3.8 
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  
### Installation
Using pip to install in editable mode seems the cleanest way to avoid pythons import troubles. Editable allows one to make changes to the repository and have them instantly available in their applicaton. As an aside, using pip install -e . works perfectly well for both python-ivi and the python-vxi11 repositories as well.
    clone
    cd into repository
    pip install -e .

If pip refuses to install with an 'editable mode' error, see [here](https://stackoverflow.com/a/73779542) for upgrading pip.

### Notes
  * developed for an HP3488A with an E2050A GPIB/ethernet bridge
  * routing is incredibly simplistic
  * with my older instruments, i had to define instr.term_char = '\n'.  I found
    this caused a conversion error during pack_int() of the python-vxi11
    library.  If you have the same problem, notes on how i worked around it
    are [here](https://github.com/python-ivi/python-vxi11/pull/26/commits/d6205bf8dd298a5b629304e5853595510519432c)

This has been a fun trip and I appreciate the work the Python-IVI
developers have invested.

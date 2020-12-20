# hp3488-ivi
HP3488 Switch/Control Unit driver for Python-IVI

A simple but functional driver for interacting with the HP 3488A and 3499A Switch/Control Unit

The HP 3488A is a modern styled (pre Agilent) rack for various switch modules often used for routing signals between 
devices for product development or test.

This driver is composed of a driver for each plugin and the 3488A rack itself.  The following plugins are functional:
  * 44470A Ten Channel Differential Mux
  * 44472A Dual Four Channel VHF Mux
  * 44473A 4 X 4 Matrix Switch

No work has been done on the 3488A driver itself which would conceivably implement some sort of smart routing between plugins.
Very much a work in progress.  

### Requirements
  * developed and tested with Python3.8 
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  
### Installation

The typical (and perhaps easiest) way to install found ivi drivers is to comingle them In-Tree with IVI's supplied drivers
#### In Tree ####
  * copy the drivers to the python-ivi/ivi/agilent folder.
  * edit the agilent/__init__.py file to allow python to find your new drivers.
  * rebuild and reinstall python-ivi.
  * fiddle with the example code.

If you prefer to keep them more separate, this method works well:
#### In Tree but separate ####
  * see this [gist](https://gist.github.com/coburnw/57634c7e821dd7f32e9a68e1d14c16a4)
  
### Notes
  * developed for an HP3488A with an E2050A GPIB/ethernet bridge
  * if any of the agilent3488 driver files are modified, python-ivi will
    need to be rebuilt and reinstalled
  * routing is incredibly simplistic
  * with my older instruments, i had to define instr.term_char = '\n'.  I found
    this caused a conversion error during pack_int() of the python-vxi11
    library.  If you have the same problem, notes on how i worked around it
    are [here](https://github.com/python-ivi/python-vxi11/pull/26/commits/d6205bf8dd298a5b629304e5853595510519432c)

This has been a fun trip and I appreciate the work the Python-IVI
developers have invested.

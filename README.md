# hp3488-ivi
HP3488 Switch/Control Unit driver for Python-IVI

A simple but functional driver for interacting with the HP 3488A and 3499A
Switch/Control Unit and their plugins.

The HP 3488A is a modern styled (pre Agilent) rack for various
switch modules often used for routing signals between 
devices for product development or test.

This repository is composed of a driver for each plugin and the 3488A rack
itself.  The following plugins are functional:
  * 44470A Ten Channel Differential Mux
  * 44472A Dual Four Channel VHF Mux

The plugin drivers are fully functional on their own meaning the rack driver does
not implement a container for the plugins.  Configure the driver_settings
dictionary with the slot and group id, along with any card specific options.  Use
the example program to get started.

These drivers use the Legacy HP3488 command set.  To use with the more modern HP3499 model,
use the front panel to set its mode to 3488.  Hooks have been implemented for someone with the 
newer scpi enabled rack to implement if needed.

The HP34xx_Plugin class implements the vast majority of the ivi boiler plate needed
for a plugin card driver.  Derive from that to greatly ease the chore of building
a driver for a new plugin card.  If you are happy with your results, consider a 
pull request to add your driver to the list of supported plugins.  

A preliminary 3488A driver has been added which currently only
exports commands unrelated to the plugins, but could conceivably implement some sort of
smart routing between cards in the future.
Very much a work in progress.  

### Requirements
  * developed and tested with Python3.8
  * extensive testing by the user before use
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  
### Installation
Using pip to install in editable mode seems the cleanest way to avoid pythons import troubles. 
Editable allows one to make changes to the repository and have them instantly available in their 
applicaton. As an aside, using `pip install -e .` works perfectly well for both python-ivi and 
the python-vxi11 repositories as well.
```
git clone https://github.com/coburnw/hp3488-ivi.git
cd hp3488-ivi
pip install -e .
```
If pip refuses to install with an 'editable mode' error, see [here](https://stackoverflow.com/a/73779542) for upgrading pip.

### Notes
  * developed for an HP3488A with an E2050A GPIB/ethernet bridge
  * no routing attempted
  * with some of my older instruments, i had to define instr.term_char = '\n'.  I found
    this caused a conversion error during pack_int() of the python-vxi11
    library.  If you have the same problem, notes on how i worked around it
    are [here](https://github.com/python-ivi/python-vxi11/pull/26/commits/d6205bf8dd298a5b629304e5853595510519432c)

This has been a fun trip and I appreciate the work the Python-IVI
developers have invested.

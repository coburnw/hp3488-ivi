# Toy to tinker with Agilent HP3488 Switch/Multiplexer using Python-IVI
#
#

import sys
import time

import ivi
from hp3488_ivi import agilent3488

##
## use IVI and the driver to interact with a vxi-11 connected instrument.
##

def printstate():
    pass

if __name__ == '__main__':

    rack = agilent3488("TCPIP0::192.168.2.9::gpib0,9::INSTR")
    print(rack.identity.instrument_model)
    rack.utility.reset()
    rack.utility.self_test()

    print()
    
    # single group card
    rack._card_monitor('4')
    #mux = rack.get_card_function(slot=4, function=0, driver_options=dict())
    mux = rack._slots[4].groups[0]
    print(mux.identity.instrument_model)
    for i in range(mux._channel_count):
        print(mux.channels[i].name)

    mux.path.connect('chan1', 'com')
    time.sleep(0.5)
    mux.path.connect('chan2', 'com')
    time.sleep(0.5)
    mux.path.connect('chan3', 'com')
    time.sleep(0.5)
    mux.path.connect('chan4', 'com')

    print()
    
    # multi group card
    rack._card_monitor('1')
    hp44472 = rack._slots[1]
    print(hp44472.identity.instrument_model)
    mux0 = hp44472.groups[0]
    mux1 = hp44472.groups[1]
    
    for i in range(mux0._channel_count):
        print(mux0.channels[i].name)

    mux0.path.connect('chan2', 'com')
    mux1.path.connect('chan1', 'com')
    
    exit()

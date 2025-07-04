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

    # single group card
    rack._card_monitor('4')
    mux = rack._slots[4]
    for i in range(mux._channel_count):
        print(mux.channels[i].name)

    mux.path.connect('channel1', 'common')
    time.sleep(0.5)
    mux.path.connect('channel2', 'common')
    time.sleep(0.5)
    mux.path.connect('channel3', 'common')
    time.sleep(0.5)
    mux.path.connect('channel4', 'common')

    # multi group card
    rack._card_monitor('1')
    hp44472 = rack._slots[1]
    mux0 = hp44472.groups[0]
    mux1 = hp44472.groups[1]
    
    for i in range(mux0._channel_count):
        print(mux0.channels[i].name)

    mux0.path.connect('chan2', 'com')
    mux1.path.connect('chan1', 'com')
    
    exit()

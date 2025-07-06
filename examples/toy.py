# Toy to tinker with Agilent HP3488 Switch/Multiplexer using Python-IVI
#
#

import sys
import time

import ivi
from hp3488_ivi import Agilent3488
from hp3488_ivi import Agilent44470
from hp3488_ivi import Agilent44472

##
## use IVI and the driver to interact with a vxi-11 connected instrument.
##

def printstate():
    pass

if __name__ == '__main__':

    rack = Agilent3488("TCPIP0::192.168.2.9::gpib0,9::INSTR")
    print(rack.identity.instrument_model)
    rack.utility.reset()
    rack.utility.self_test()

    print()
    
    # single group card
    rack._card_monitor('4')
    driver_setup = dict()
    mux = Agilent44470("TCPIP0::192.168.2.9::gpib0,9::slot4,group1::INSTR", driver_setup=driver_setup)
    print(mux.identity.instrument_model)
    for i in range(mux._channel_count):
        print(mux.channels[i].name)

    mux.path.connect('chan3', 'com')
    time.sleep(0.5)
    mux.path.connect('chan4', 'com')
    time.sleep(0.5)
    mux.path.connect('chan5', 'com')
    time.sleep(0.5)
    mux.path.connect('chan6', 'com')

    print()
    
    # multi group card
    rack._card_monitor('1')
    mux0 = Agilent44472("TCPIP0::192.168.2.9::gpib0,9::slot1,group0::INSTR", driver_setup=driver_setup)
    mux1 = Agilent44472("TCPIP0::192.168.2.9::gpib0,9::slot1,group1::INSTR", driver_setup=driver_setup)
    print(mux0.identity.description)
    
    for i in range(mux0._channel_count):
        print(mux0.channels[i].name)

    mux0.path.connect('chan2', 'com')
    mux1.path.connect('chan1', 'com')
    
    exit()

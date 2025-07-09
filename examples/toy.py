# Toy to tinker with Agilent HP3488 Switch/Multiplexer using Python-IVI
#
#

import sys
import time

import ivi
from hp3488_ivi import Agilent3488
from hp3488_ivi import Agilent3499
from hp3488_ivi import Agilent44470
from hp3488_ivi import Agilent44472

##
## use IVI and the driver to interact with a vxi-11 connected instrument.
##

def printstate():
    pass

if __name__ == '__main__':

    print('opening 3488')
    rack = Agilent3499("TCPIP0::192.168.2.9::gpib0,9::INSTR", id_query=False, simulate=True)
    print('model', rack.identity.instrument_model)
    print('desc', rack.identity.description)
    rack.utility.reset()
    rack.utility.self_test()

    print()
    
    # single group card
    rack._card_monitor('4')

    # driver setup keyword/values
    driver_setup = dict()
    #driver_setup['protocol'] = 'legacy'
    driver_setup['slot_id'] = 4
    driver_setup['group_id'] = 0

    # configure switch as a buss.
    driver_setup['is_mux'] = False

    print('opening 44470')
    mux = Agilent44470("TCPIP0::192.168.2.9::gpib0,9::INSTR", id_query=True, driver_setup=driver_setup, simulate=True)

    print('model', mux.identity.instrument_model)
    print('desc', mux.identity.description)
    for i in range(mux._channel_count):
        print(mux.channels[i].name)

    # use switch as a buss
    mux.path.connect('chan3', 'chan4')

    # reconfigure switch as a mux
    mux.driver_setup['is_mux'] = True

    # mux
    mux.path.connect('chan3', 'com')
    time.sleep(0.5)
    mux.path.connect('chan4', 'com')
    time.sleep(0.5)
    mux.path.connect('chan5', 'com')
    time.sleep(0.5)
    mux.path.connect('chan6', 'com')

    print()
    
    # multi group card
    #rack._card_monitor('1')

    # use default driver setup values
    driver_setup = dict()
    driver_setup['slot_id'] = 1
    driver_setup['group_id'] = 0
    print('opening 44472')
    mux0 = Agilent44472("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=driver_setup)
    print('model', mux0.identity.instrument_model)
    print('desc', mux0.identity.description)
    
    driver_setup['slot_id'] = 1
    driver_setup['group_id'] = 1
    print('opening 44472')
    mux1 = Agilent44472("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=driver_setup)
    print('model', mux1.identity.instrument_model)
    print('desc', mux1.identity.description)
    
    for i in range(mux1._channel_count):
        print(mux1.channels[i].name)

    mux0.path.connect('chan2', 'com')
    mux1.path.connect('chan1', 'com')
    
    exit()

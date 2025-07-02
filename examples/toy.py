# Toy to tinker with Agilent HP3488 Switch/Multiplexer using Python-IVI
#
#

import sys
import time

import ivi
from hp3488_ivi import agilent3488
from hp3488_ivi import agilent44470
from hp3488_ivi import agilent44472

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
    
    exit()
    
    board = rack._slots[1]
    for i in range(board._channel_count):
        print(board.channels[i].name)
        
    # rack.path.connect('1!0-chan2', '1!0-com')
    # rack.path.connect('1!1-chan2', '1!1-com')
    #rack.path.connect('slot1.sect0.chan2', 'slot1.sect0.chan5')
    rack.path.connect('102', '105')
    rack.path.connect('112', '115')
    exit()

    config_slot_1a = {'slot_id':1, 'group_id':0}
    config_slot_1b = {'slot_id':1, 'group_id':1}
    bnc_a = agilent44472("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=config_slot_1a)
    bnc_b = agilent44472("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=config_slot_1b)
    
    config_slot_4 = {'slot_id':4, 'group_id':0, 'is_mux':True}
    mux = agilent44470("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=config_slot_4)

    #mux.help()
    #dvm.driver_operation.simulate = False

    #print(mux.identity.instrument_firmware_revision)
    #print(mux.identity.instrument_serial_number)
    #print(mux.identity.supported_instrument_models)
    print(mux.identity.group_capabilities)
    print(mux.identity.identifier)

    #print('initiating self test: ') 
    #mux.utility.self_test()

    print(mux.identity.description)
    print(mux.identity.instrument_manufacturer),
    print(mux.identity.instrument_model),
    print(' has ' + str(len(mux.channels)) + ' channels.')
    mux.path.connect('channel0','common')
    time.sleep(1)
    mux.path.connect('channel1','common')
    time.sleep(1)
    mux.path.connect('channel2','common')
    time.sleep(1)
    mux.path.connect('channel3','common')
    time.sleep(1)
    mux.path.disconnect('channel3','common')
    time.sleep(1)
    print()
    
    print(bnc_a.identity.description)
    print(bnc_a.identity.instrument_manufacturer),
    print(bnc_a.identity.instrument_model),
    print(' has ' + str(len(bnc_a.channels)) + ' channels.')
    bnc_a.path.connect('channel0','common')
    time.sleep(1)
    bnc_a.path.connect('channel1','common')
    time.sleep(1)
    bnc_a.path.connect('channel2','common')
    time.sleep(1)
    bnc_a.path.connect('channel3','common')
    time.sleep(1)
    bnc_a.path.disconnect('channel3','common')

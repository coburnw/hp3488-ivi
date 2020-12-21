# Toy to tinker with Agilent HP3488 Switch/Multiplexer using Python-IVI
#
#

import sys
import time

import ivi

##
## use IVI and the driver to interact with a vxi-11 connected instrument.
##

def printstate():
    pass

if __name__ == '__main__':
    config_slot_1a = {'slot_id':1, 'group_id':0}
    config_slot_1b = {'slot_id':1, 'group_id':1}
    bnc_a = ivi.local.agilent44472("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=config_slot_1a)
    bnc_b = ivi.local.agilent44472("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=config_slot_1b)
    
    config_slot_4 = {'slot_id':4, 'group_id':0, 'is_mux':True}
    mux = ivi.local.agilent44470("TCPIP0::192.168.2.9::gpib0,9::INSTR", driver_setup=config_slot_4)

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

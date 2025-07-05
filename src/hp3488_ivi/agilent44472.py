"""

Python Interchangeable Virtual Instrument Library

agilent44472.py
Copyright (c) 2017-2025 Coburn Wightman

Derived from rigolDP800.py 
Copyright (c) 2013-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import ivi
from ivi import swtch
         
class agilent44472(ivi.Driver, swtch.Base):
    "Agilent HP44472 IVI VHF Dual Mux Board"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        # python-vxi11 doesnt like the 'slot' in the resource string.
        # extract it and clean up the resource string before ivi.Driver.init() 
        self._slot_id, args = self._extract_slot_id(args)
        super().__init__(*args, **kwargs)

        self._identity_description = "Agilent HP44472 Dual 4-Channel VHF Switch Module"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent"
        self._identity_instrument_model = "HP44472"
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['HP44472']

        if 'driver_setup' not in kwargs.keys():
            kwargs['driver_setup'] = dict()
            
        self.groups = []
        kwargs['driver_setup']['group_id'] = 0
        self.groups.append(Agilent44472Mux(*args, **kwargs))
        kwargs['driver_setup']['group_id'] = 1
        self.groups.append(Agilent44472Mux(*args, **kwargs))
        
        return

    def _extract_slot_id(self, args): # args is a tuple
        # converts args to a list, extracts the slotid, returns a sanatized tuple
        lst = list(args)

        idx = lst[0].rfind('slot')
        slot_id = lst[0][idx+len('slot')]
        lst[0] = lst[0].replace('slot{}::'.format(slot_id), '')

        args = tuple(lst)
        return slot_id, args
    
    
class Agilent44472Mux(ivi.Driver, swtch.Base):
    "Agilent HP44472 IVI VHF Mux Group"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')        
        super().__init__(*args, **kwargs)

        self._identity_description = "Agilent HP44472 4-Channel VHF Switch Group"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent"
        self._identity_instrument_model = "HP44472"
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['HP44472']
        
        driver_setup = kwargs.get('driver_setup', dict())
        self._slot_id = driver_setup.get('slot_id', 1)        
        self._group_id = driver_setup.get('group_id', 0)

        return

    def _init_channels(self):
        self._channel_count = 4+1

        try:
            super()._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_is_configuration_channel = list()
        self._channel_is_source_channel = list()
        self._channel_characteristics_ac_current_carry_max = list()
        self._channel_characteristics_ac_current_switching_max = list()
        self._channel_characteristics_ac_power_carry_max = list()
        self._channel_characteristics_ac_power_switching_max = list()
        self._channel_characteristics_ac_voltage_max = list()
        self._channel_characteristics_bandwidth = list()
        self._channel_characteristics_impedance = list()
        self._channel_characteristics_dc_current_carry_max = list()
        self._channel_characteristics_dc_current_switching_max = list()
        self._channel_characteristics_dc_power_carry_max = list()
        self._channel_characteristics_dc_power_switching_max = list()
        self._channel_characteristics_dc_voltage_max = list()
        self._channel_characteristics_settling_time = list()
        self._channel_characteristics_wire_mode = list()
        
        for channel_index in range(self._channel_count):
            self._channel_name.append('chan{}'.format(channel_index))
            self._channel_is_configuration_channel.append(False)
            self._channel_is_source_channel.append(False)
            self._channel_characteristics_ac_current_carry_max.append(0.1)
            self._channel_characteristics_ac_current_switching_max.append(0.1)
            self._channel_characteristics_ac_power_carry_max.append(1)
            self._channel_characteristics_ac_power_switching_max.append(1)
            self._channel_characteristics_ac_voltage_max.append(100)
            self._channel_characteristics_bandwidth.append(100e6)
            self._channel_characteristics_impedance.append(50)
            self._channel_characteristics_dc_current_carry_max.append(0.1)
            self._channel_characteristics_dc_current_switching_max.append(0.1)
            self._channel_characteristics_dc_power_carry_max.append(1)
            self._channel_characteristics_dc_power_switching_max.append(1)
            self._channel_characteristics_dc_voltage_max.append(100)
            self._channel_characteristics_settling_time.append(0.1)
            self._channel_characteristics_wire_mode.append(2)

        # convert last channel to mux common
        self._channel_name[channel_index] = 'com'
        self._channel_is_configuration_channel[channel_index] = True
        
        self.channels._set_list(self._channel_name)    
        return

    def set_driver_options(self, **kwargs):
        pass
    
    def _name_to_address(self, channel_name):
        channel_index = ivi.get_index(self._channel_name, channel_name)
        channel_address = self._slot_id*100 + self._group_id*10 + channel_index
        
        return channel_address
        
    def _chan_connect(self, channel_name):
        channel_address = self._name_to_address(channel_name)

        # com channel is always connected.  quietly ignore
        if 'com' not in channel_name.lower():
            print('connecting {} to Common'.format(channel_address))
            cmd = ' CLOSE' + str(channel_address)
            self._write(cmd)

        return

    def _chan_disconnect(self, channel_name):
        channel_address = self._name_to_address(channel_name)

        # com channel is always connected.  quietly ignore
        if 'com' not in channel_name.lower():
            print('disconnecting ' + str(channel_address) + ' from ' + 'Common')
            cmd = ' OPEN' + str(channel_address)
            self._write(cmd)
            
        return
                
    def _path_can_connect(self, channel1, channel2):
        # let get_index raise if invalid channel
        chan1 = ivi.get_index(self._channel_name, channel1)
        chan2 = ivi.get_index(self._channel_name, channel2)

        if chan1 == chan2:
            raise swtch.CannotConnectToItselfException
        elif 'com' not in channel1.lower() and 'com' not in channel2.lower():
            raise swtch.InvalidSwitchPathException("valid paths must contain a 'common' channel")

        return True
    
    def _path_connect(self, channel1, channel2):
        if self._path_can_connect(channel1, channel2):
            self._chan_connect(channel1)
            self._chan_connect(channel2)
        return
        
    def _path_disconnect(self, channel1, channel2):
        if self._path_can_connect(channel1, channel2):
            self._chan_disconnect(channel1)
            self._chan_disconnect(channel2)
        return
        
    def _path_disconnect_all(self):
        cmd = ' CRESET' + str(self._slot_id)
        if self._driver_operation_simulate:
            print(cmd)
        else:
            self._write(cmd)
            
    def _path_get_path(self, channel1, channel2):
        channel1 = ivi.get_index(self._channel_name, channel1)
        channel2 = ivi.get_index(self._channel_name, channel2)
        return []
    
    def _path_set_path(self, path):
        pass
    
    def _path_wait_for_debounce(self, maximum_time):
        pass

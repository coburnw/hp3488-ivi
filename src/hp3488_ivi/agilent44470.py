"""

Python Interchangeable Virtual Instrument Library

agilent44470.py
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
from .agilent3488 import Agilent3488_Plugin
         
class Agilent44470(Agilent3488_Plugin):
    '''Agilent HP44470 IVI 10 Channel Mux Board'''
    
    def __init__(self, *args, **kwargs):
        # hide a definition of supported models from ivi
        self.__dict__.setdefault('_driver_supported_models', ['44470'])
        
        super().__init__(*args, **kwargs)

        self._identity_description = "Agilent HP44470 Ten Channel Mux Board, Group 0"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent"
        self._identity_instrument_model = "HP44470"
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = self._driver_supported_models
        
        if 'is_mux' not in self.driver_setup:
            self.driver_setup['is_mux'] = True

        if self.group_id < 0 or self.group_id > 0:
            raise ivi.OutOfRangeException('device contains only one switch group (group0)')

        self._load_identity()

        return

    def _init_channels(self):
        # our switch group has ten channels plus a common
        self._channel_count = 10
        
        try:
            super()._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
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
        self._channel_is_configuration_channel = list()
        self._channel_is_source_channel = list()
        self._channel_characteristics_settling_time = list()
        self._channel_characteristics_wire_mode = list()

        #print('adding {} channels'.format(self._channel_count))
        # configure channel_count+com channels 
        for i in range(self._channel_count+1):
            #print('adding channel {}'.format(i))
            self._channel_name.append("chan%d" % (i))
            self._channel_characteristics_ac_current_carry_max.append(2.0)
            self._channel_characteristics_ac_current_switching_max.append(0.1)
            self._channel_characteristics_ac_power_carry_max.append(500)
            self._channel_characteristics_ac_power_switching_max.append(1)
            self._channel_characteristics_ac_voltage_max.append(250)
            self._channel_characteristics_bandwidth.append(10e6)
            self._channel_characteristics_impedance.append(50)
            self._channel_characteristics_dc_current_carry_max.append(2.0)
            self._channel_characteristics_dc_current_switching_max.append(0.1)
            self._channel_characteristics_dc_power_carry_max.append(60)
            self._channel_characteristics_dc_power_switching_max.append(1)
            self._channel_characteristics_dc_voltage_max.append(250)
            self._channel_is_configuration_channel.append(False)
            self._channel_is_source_channel.append(False)
            self._channel_characteristics_settling_time.append(0.1)
            self._channel_characteristics_wire_mode.append(2)

        #print(' converting channel {} to common'.format(i))
        self._channel_name[i] = 'com'
        self._channel_is_configuration_channel[i] = True
        
        self.channels._set_list(self._channel_name)
        return

    def _name_to_address(self, channel_name):
        channel_index = ivi.get_index(self._channel_name, channel_name)
        channel_address = self.slot_id * 100 + self.group_id * 10 + channel_index

        return channel_address
        
    def _chan_connect(self, channel):
        #print('connecting ' + str(channel) + ' to ' + 'Common')
        channel_address = self._name_to_address(channel)

        if self.driver_setup['is_mux']:
            cmd = ' CHAN' + str(channel_address)
        else:
            cmd = ' CLOSE' + str(channel_address)
                    
        if self._driver_operation_simulate:
            print(cmd)
        else:
            self._write(cmd)

        return

    def _chan_disconnect(self, channel):
        channel_address = self._name_to_address(channel)

        if self.driver_setup['is_mux']:
            self._path_disconnect_all()
        else:
            cmd = ' OPEN' + str(channel_address)
            if self._driver_operation_simulate:
                print(cmd)
            else:
                self._write(cmd)
            
        return
        
    def _path_can_connect(self, channel1, channel2):
        # get_index will raise if channel invalid
        chan1 = ivi.get_index(self._channel_name, channel1)
        chan2 = ivi.get_index(self._channel_name, channel2)
        
        if chan1 == chan2:
            raise swtch.CannotConnectToItselfException
        elif self.driver_setup['is_mux'] and (chan1 != self._channel_count) and (chan2 != self._channel_count):
            raise swtch.InvalidSwitchPathException("in mux mode, valid paths must contain a 'common' channel")
        
        return True

    def _path_connect(self, channel1, channel2):
        if self._path_can_connect(channel1, channel2):
            if 'com' not in channel1:
                self._chan_connect(channel1)
            if 'com' not in channel2:
                self._chan_connect(channel2)
            
        return

    def _path_disconnect(self, channel1, channel2):
        self._chan_disconnect(channel1)
        self._chan_disconnect(channel2)
        
        return
        
    def _path_disconnect_all(self):
        cmd = ' CRESET' + str(self.slot_id)
        
        if self._driver_operation_simulate:
            print(cmd)
        else:
            self._write(cmd)
            
        return
            
    def _path_wait_for_debounce(self, maximum_time):
        pass

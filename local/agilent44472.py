"""

Python Interchangeable Virtual Instrument Library

agilent44472.py
Copyright (c) 2017 Coburn Wightman

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

from .. import ivi
from .. import swtch
         
class agilent44472(ivi.Driver, swtch.Base):
    "Agilent HP44472 IVI VHF Mux Option Board"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(agilent44472, self).__init__(*args, **kwargs)

        driver_setup = kwargs.get('driver_setup', dict())
        self._slot_id = driver_setup.get('slot_id', 1)
        self._group_id = driver_setup.get('group_id', 0)
        
        self._group_count = 2

        self._identity_description = "Agilent HP44472 IVI VHF Mux driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent"
        self._identity_instrument_model = "HP44472"
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['HP44472']
        
        #self._init_channels()
        return

    def _init_channels(self):
        # 4 channels plus common
        self._channel_count = 4+1

        try:
            super(agilent44472, self)._init_channels()
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

        for i in range(self._channel_count):
            self._channel_name.append("channel%d" % (i))
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
            self._channel_is_configuration_channel.append(False)
            self._channel_is_source_channel.append(False)
            self._channel_characteristics_settling_time.append(0.1)
            self._channel_characteristics_wire_mode.append(2)

        self._channel_name[i] = 'common'
        self._channel_is_configuration_channel[i] = True
        
        self.channels._set_list(self._channel_name)    
        return
    
    def _chan_connect(self, channel):
            channel_index = ivi.get_index(self._channel_name, channel)
            if channel_index < self._channel_count - 1:
                channel_address = self._slot_id * 100 + self._group_id * 10 + channel_index
                #print('connecting ' + str(channel_address) + ' to ' + 'Common')
                cmd = ' CLOSE' + str(channel_address)
                    
                if self._driver_operation_simulate:
                    print(cmd)
                else:
                    self._write(cmd)

            return

    def _chan_disconnect(self, channel):
            channel_index = ivi.get_index(self._channel_name, channel)
            if channel_index < self._channel_count - 1:
                channel_address = self._slot_id * 100 + self._group_id * 10 + channel_index
                #print('disconnecting ' + str(channel_address) + ' from ' + 'Common')
                cmd = ' OPEN' + str(channel_address)
                    
                if self._driver_operation_simulate:
                    print(cmd)
                else:
                    self._write(cmd)
            return
        
        
    def _path_can_connect(self, channel1, channel2):
        # let get_index raise if invalid channel
        chan1 = ivi.get_index(self._channel_name, channel1)
        chan2 = ivi.get_index(self._channel_name, channel2)

        if chan1 == chan2:
            raise swtch.CannotConnectToItselfException
        elif chan1 != self._channel_count-1 and chan2 != self._channel_count-1:
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

"""

Python Interchangeable Virtual Instrument Library

agilent3488.py
Copyright (c) 2020-2025 Coburn Wightman

Derived from rigolDP800.py 
Copyright (c) 2012-2017 Alex Forencich

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

import struct

import ivi
from ivi import swtch

#from .agilent44470 import Agilent44470 as C44470
#from .agilent44471 import Agilent44471 as C44471
#from .agilent44472 import Agilent44472 as C44472


class Agilent3488_Plugin(ivi.Driver, swtch.Base):
    ''' Base class for Agilent 3488/3499 Plug-in boards '''
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        # python-vxi11 doesnt like 'slot' in the resource string.
        # extract it and clean up the resource string 
        resource_string = args[0]
        self._slot_id, self._group_id, resource_string = self._extract_slot_params(resource_string)
        print(self._slot_id, self._group_id, resource_string)

        #replace resource_string with sanitized version
        lst = list(args)
        lst[0] = resource_string
        args = tuple(lst)
        
        super().__init__(*args, **kwargs)

        if 'driver_setup' not in kwargs.keys():
            kwargs['driver_setup'] = dict()

        self._driver_setup = kwargs['driver_setup']
        
        return

    def _extract_slot_params(self, resource_string):
        slot_id = 0
        group_id = 0
        
        # extracts the slotid from args list, returns a sanatized tuple
        segments = resource_string.split('::')
        rsc = ''
        for segment in segments:
            if 'slot' in segment:
                slot_params = segment.strip(':').split(',')
                if len(slot_params) > 0:
                    slot_id = int(slot_params[0].replace('slot', ''))
                if len(slot_params) > 1:
                    group_id = int(slot_params[1].replace('group', ''))
                segment = ''
            else:
                rsc += segment + '::'

        resource_string = rsc.rstrip(':')
        return slot_id, group_id, resource_string

    @property
    def slot_id(self):
        return self._slot_id

    @property
    def group_id(self):
        return self._group_id

    @property
    def driver_setup(self):
        return self._driver_setup
    
class Agilent3488(ivi.Driver, swtch.Base):
    "Agilent HP3488 Switch driver"

    def __init__(self, *args, **kwargs):
        print('enter init()')
        self._resource_string = args[0]
        
        # other per-channel instrument-specific variables that are
        # referenced in _init_channels

        super().__init__(*args, **kwargs)

        print(' configuring instrument')
        
        self._instrument_id = 'HP3488'
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 16
        self._channel_count = 20
        self._bandwidth = 1e9
        # initialize other instrument-specific variables

        self._identity_description = "Agilent HP3488/HP3499 series Switch/Control Unit"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models =['HP3488A','HP3488B','HP3488R','HP3499A','HP3499B','HP3499C']

        # check ID
        if not self._driver_operation_simulate:
            print(' checking identity')
            id = self.identity.instrument_model
            if id not in self._identity_supported_instrument_models:
                raise Exception("Instrument ID mismatch: got {}, expected one of {}.", id,
                                self._identity_supported_instrument_models)
            self._instrument_id = id
            print('found supported instrument: {}'.format(self.identity.instrument_model))

        #self._load_cards()    # discover installed cards
        #self._init_channels() # build database of possible connection endpoints
        
        print('exit init()')
        return

    def _init_channels(self):
        print('enter init_channels()')
        if not self._instrument_id:
            print(' skipping')
            return
        
        super()._init_channels()

        self._channel_name = list()
        self._channel_label = list()

        self.channels._set_list(self._channel_name)

        print('exit init_channels()')
        return
    
    # def _load_cards(self):
    #     print('enter load_cards()')
        
    #     self._slots = dict()
    #     for slot_id in range(1,6):
    #         slot_resource_string = self._append_slot_id(self._resource_string, slot_id)
            
    #         card_type = self._card_type_query(slot_id)
    #         if '00000' in card_type:
    #             card = None
    #         elif '44470' in card_type:
    #             card = C44470(slot_resource_string)
    #         elif '44471' in card_type:
    #             #card = C44471(slot_resource_string)
    #             card = None
    #         elif '44472' in card_type:
    #             card = C44472(slot_resource_string)
    #         elif '44473' in card_type:
    #             card = None
    #         else:
    #             card = None
                    
    #         self._slots[slot_id] = card
    #         card_description = 'Empty'
    #         if card:
    #             card_description = card.identity.description

    #         print('slot {} contains {}'.format(slot_id, card_description))
            
    #     print('exit load_cards()')
    #     return

    def _load_id_string(self):
        print('  load_id_string()')
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._ask("ID?").split(",")
            print('   found: {}'.format(lst))
            
            if len(lst) == 1:
                self._identity_instrument_model = lst[0]
                self._set_cache_valid(True, 'identity_instrument_model')
            else:
                self._identity_instrument_manufacturer = lst[0]
                self._identity_instrument_model = lst[1]
                self._identity_instrument_firmware_revision = lst[3]
                self._set_cache_valid(True, 'identity_instrument_manufacturer')
                self._set_cache_valid(True, 'identity_instrument_model')
                self._set_cache_valid(True, 'identity_instrument_firmware_revision')

        print('  leaving load_id_string())')
        return
    
    def _get_identity_instrument_manufacturer(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_model

    def _get_identity_instrument_firmware_revision(self):
        if not self._get_cache_valid():
            self._load_id_string()
        return self._identity_instrument_firmware_revision

    def _card_type_query(self, slot):
        print ('  enter _card_type_query()')
        card_type = 'No card in simulate mode'
        if not self._driver_operation_simulate:
            cmd = 'CTYPE {}'.format(slot)
            card_type = self._ask(cmd)
            
        return (card_type)
    
    def _card_reset(self, slot):
        cmd = 'CRESET {}'.format(slot)
        self._write(cmd)
        return

    def _card_pair(self, slot_a, slot_b):
        cmd = 'CPAIR {},{}'.format(slot_a, slot_b)
        self._write(cmd)
        return

    def _card_monitor(self, slot):
        cmd = 'CMON {}'.format(slot)
        self._write(cmd)
        return

    def get_card_function(self, slot_index, function_index, driver_options):
        function = self.slots[slot_index][function_index]
        function.set_driver_options(driver_options)
        
        return function
    
    def _utility_disable(self):
        pass

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            #error_code, error_message = self._ask("error").split(',')
            error_code = self._ask("ERROR")
            error_code = int(error_code)
            error_message = 'no message'
            #error_message = error_message.strip(' "')
        return (error_code, error_message)

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("RESET")
            self.driver_operation.invalidate_all_attributes()
        return

    def _utility_reset_with_defaults(self):
        self._utility_reset()
        return

    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            code = int(self._ask("TEST"))
            if code != 0:
                message = "Self test failed"
        return (code, message)

    def _get_acquisition_start_time(self):
        pos = 0
        if not self._driver_operation_simulate and not self._get_cache_valid():
            pos = float(self._ask(":timebase:position?"))
            self._set_cache_valid()
        self._acquisition_start_time = pos - self._get_acquisition_time_per_record() * 5 / 10
        return self._acquisition_start_time

    def _set_acquisition_start_time(self, value):
        value = float(value)
        value = value + self._get_acquisition_time_per_record() * 5 / 10
        if not self._driver_operation_simulate:
            self._write(":timebase:position %e" % value)
        self._acquisition_start_time = value
        self._set_cache_valid()

    def parse_channel_address(self, address_string):
        addr = int(address_string)

        slot = addr // 100
        if slot < 1 or slot > 5:
            raise swtch.InvalidSwitchPathException
            
        chan = addr - slot * 100
        return slot, chan

    # between board paths
    def _path_can_connect(self, channel_a, channel_b):
        # get_index will raise if channel invalid
        slot_a, chan_a = self.parse_channel_address(channel_a)
        slot_b, chan_b = self.parse_channel_address(channel_b)
                                           
        print('checking path {}.{} -> {}.{}'.format(slot_a, chan_a, slot_b, chan_b))
        if slot_a != slot_b:
            raise swtch.NoSuchPathException

        return self._slots[slot_a].path.can_connect(chan_a, chan_b)

    def _path_connect(self, channel_a, channel_b):

        if self._path_can_connect(channel_a, channel_b):
            slot_a, chan_a = self.parse_channel_address(channel_a)
            slot_b, chan_b = self.parse_channel_address(channel_b)

            card = self._slots[slot_a]
            card.path.connect(chan_a, chan_b)

        return

    def _path_get_path(self, channel1, channel2):
        # channel1 = ivi.get_index(self._channel_name, channel1)
        # channel2 = ivi.get_index(self._channel_name, channel2)

        return []
    
    def _path_set_path(self, path):
        pass
    

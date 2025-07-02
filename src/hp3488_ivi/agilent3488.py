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

from .agilent44470 import agilent44470 as C44470
from .agilent44472 import agilent44472 as C44472

AcquisitionTypeMapping = {
        'normal': 'norm',
        'peak_detect': 'peak',
        'high_resolution': 'hres',
        'average': 'aver'}
# more instrument-specific sets and mappings

class agilent3488(ivi.Driver, swtch.Base):
    "Agilent HP3488 Switch driver"

    def __init__(self, *args, **kwargs):
        print('enter init()')
        self._resource_string = args[0]
        
        # self._slots = list()
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

        self._identity_description = "Agilent HP3488 series IVI switch driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models =['HP3488A','HP3488B','HP3488R']

        # self.channels._add_property('label',
        #                 self._get_channel_label,
        #                 self._set_channel_label,
        #                 None,
        #                 """
        #                 Custom property documentation
        #                 """)

        # other instrument specific properties

        # check ID
        if not self._driver_operation_simulate:
            print(' checking identity')
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)
            print('instrument id check: expecting {}, got {}'.format(id_check, id_short))
            
        self._init_channels()
        print('exit init()')
        return

    # def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
    #     "Opens an I/O session to the instrument."
    #     print('enter initialize() {}'.format())
    #     #self._channel_count = self._analog_channel_count + self._digital_channel_count

    #     super(agilent3488, self).initialize(resource, id_query, reset, **keywargs)

    #     # interface clear
    #     if not self._driver_operation_simulate:
    #         self._clear()

    #     # check ID
    #     if id_query and not self._driver_operation_simulate:
    #         id = self.identity.instrument_model
    #         id_check = self._instrument_id
    #         id_short = id[:len(id_check)]
    #         if id_short != id_check:
    #             raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)

    #     # reset
    #     if reset:
    #         self.utility.reset()

    #     print('exit initialize()')

    #     return

    def _init_channels(self):
        print('enter init_channels()')
        if not self._instrument_id:
            print(' skipping')
            return
        
        super()._init_channels()

        self._slots = dict()

        if self._identity_instrument_model == 'HP3488A':
            for slot_id in range(1,6):
                card = None
                card_type = self._card_type_query(slot_id)
                driver_setup = {'slot_id':slot_id, 'group_id':0}
                if '00000' in card_type:
                    card = None
                elif '44470' in card_type:
                    card = C44470(self._resource_string, driver_setup=driver_setup)
                elif '44471' in card_type:
                    card = None
                elif '44472' in card_type:
                    card = C44472(self._resource_string, driver_setup=driver_setup)
                elif '44473' in card_type:
                    card = None
                else:
                    card = None
                    
                self._slots[slot_id] = card
                card_description = 'Empty'
                if card:
                    card_description = card.identity.description
                print('slot {} contains {}'.format(slot_id, card_description))
            
        self._channel_name = list()
        self._channel_label = list()
        # init per-channel instrument-specific variables

        # for i in range(self._channel_count):
        #     self._channel_name.append("channel%d" % (i+1))
        #     self._channel_label.append("%d" % (i+1))
        #     # init per-channel instrument-specific variables

        self.channels._set_list(self._channel_name)

        print('exit init_channels()')

        return

    
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
        print ('  enter get_identity_slot_card_type()')
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
            merror_message = 'no message'
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

    # more definitions
    # def parse_channel_address(self, address_string):
    #     if '!' not in address_string:
    #         raise ValueError('malformed channel address: {}'.format(address_string))
        
    #     address = address_string.partition('!')
    #     slot = address[0].strip().lower()
    #     chan = address[2].strip().lower()
    #     if int(slot) < 1 or int(slot) > 5:
    #         raise swtch.InvalidSwitchPathException
            
    #     slot = int(slot)
        
    #     return slot, chan

    def parse_channel_address(self, address_string):
        addr = int(address_string)

        slot = addr // 100
        if slot < 1 or slot > 5:
            raise swtch.InvalidSwitchPathException
            
        chan = addr - slot * 100
        return slot, chan
        
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

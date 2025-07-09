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

import ivi
from ivi import swtch


''' 
the ivi.Driver is prone to a settings race during initialization as _initialization()
is called during __init__().  Be sure to have any variables used in _initialize()
and related fully defined before calling super()__init__() to prevent odd error messages
'''


class Agilent34xx_Driver(ivi.Driver): #, swtch.Base
    ''' Base class shared by both the rack and its plugins '''

    def __init__(self, *args, **kwargs):
        self._protocol = 'legacy'
        # if 'protocol' in kwargs.keys():
        #     self._protocol = kwargs.pop('protocol')
        #     print('popping ', self.protocol)

        super().__init__(*args, **kwargs)
        print('driver operation simulate = {}'.format(self._driver_operation_simulate))

        return
    
    @property
    def protocol(self):
        return self._protocol

    def _initialize(self, resource = None, id_query = False, reset = False, **kwargs):
        "Opens an I/O session to the instrument."
        super()._initialize(resource, id_query, reset, **kwargs)
        
        # configure interface
        if self._interface is not None:
            self._interface.term_char = '\n'
        
        # interface clear
        if not self._driver_operation_simulate:
            self._clear()
        
        # check ID
        if id_query and not self._driver_operation_simulate:
            model = self.identity.instrument_model
            
            # in order to overcome a settings race during driver initialization,
            # we use the driver_supported_models defined outside ivi's view
            is_supported = False
            for supported_model in self._driver_supported_models:
                if supported_model in model:
                    is_supported = True
                    
            if not is_supported:
                raise ivi.IdQueryFailedException("Instrument ID mismatch. found {}, expected one of {}".format(model, self._driver_supported_models))
        
        # reset
        if reset:
            self.utility_reset()

        return
    
    def _get_identity_instrument_manufacturer(self):
        if not self._get_cache_valid():
            self._load_identity()
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if not self._get_cache_valid():
            self._load_identity()
        return self._identity_instrument_model

    def _get_identity_instrument_firmware_revision(self):
        if not self._get_cache_valid():
            self._load_identity()
        return self._identity_instrument_firmware_revision

    def _device_write(self, cmd):
        if self._driver_operation_simulate:
            print('  sim: {}'.format(cmd))
        else:
            self._write(cmd)

        return

    def _device_ask(self, cmd):
        if self._driver_operation_simulate:
            result = 'in simulation mode'
            print('  sim: {}'.format(cmd))
        else:
            result = self._ask(cmd)

        return result

    def _rack_id(self):
        if self.protocol == 'scpi':
            cmd = 'scpi rack id cmd'
        else:
            cmd = "ID?"

        return self._device_ask(cmd)

    def _rack_error(self):

        if self.protocol == 'scpi':
            cmd = 'scpi rack error cmd'
        else:
            cmd = 'ERROR'

        return self._device_ask(cmd)

    def _rack_reset(self):
        if self.protocol == 'scpi':
            cmd = 'scpi rack reset cmd'
        else:
            cmd = "RESET"

        self._device_write(cmd)

        return

    def _rack_test(self):
        if self.protocol == 'scpi':
            cmd = 'scpi rack test'
        else:
            cmd = "TEST"

        return self._device_ask(cmd)

    def _card_type_query(self, slot):
        card_type = 'No card in simulate mode'

        if self.protocol == 'scpi':
            cmd = 'scpi card type cmd'
        else:
            cmd = 'CTYPE {}'.format(slot)

        card_type = self._device_ask(cmd)

        parts = card_type.split(' ')
        card_type = parts[-1]
            
        return card_type
    
    def _card_reset(self, slot):
        if self.protocol == 'scpi':
            cmd = 'scpi card reset cmd'
        else:
            cmd = 'CRESET {}'.format(slot)

        self._device_write(cmd)

        return

    def _card_monitor(self, slot):
        if self.protocol == 'scpi':
            cmd = 'scpi card monitor cmd'
        else:
            cmd = 'CMON {}'.format(slot)

        self._device_write(cmd)

        return

    def _card_pair(self, slot_a, slot_b):
        if self.protocol == 'scpi':
            cmd = 'scpi card pair cmd'
        else:
            cmd = 'CPAIR {},{}'.format(slot_a, slot_b)

        self._device_write(cmd)

        return

    def _chan_open(self, channel_address):
        if self.protocol == 'scpi':
            cmd = 'scpi chan open cmd'
        else:
            cmd = 'OPEN' + str(channel_address)

        self._device_write(cmd)

        return

    def _chan_close(self, channel_address):
        if self.protocol == 'scpi':
            cmd = 'scpi chan close cmd'
        else:
            cmd = 'CLOSE' + str(channel_address)

        self._device_write(cmd)
        return

    def _chan_step(self, channel_address=None):
        if self.protocol == 'scpi':
            cmd = 'scpi chan step cmd'
        elif not channel_address:
            cmd = 'STEP'
        else:
            cmd = 'CHAN' + str(channel_address)

        self._device_write(cmd)
        return

class Agilent34xx_Plugin(Agilent34xx_Driver, swtch.Base): #
    ''' Base class for Agilent 3488/3499 Plug-in boards '''
    
    def __init__(self, *args, **kwargs):
        if 'driver_setup' not in kwargs.keys():
            kwargs['driver_setup'] = dict()

        self._driver_setup = kwargs['driver_setup']
        self._slot_id = self._driver_setup.get('slot_id', 1)
        self._group_id = self._driver_setup.get('group_id', 0)

        super().__init__(*args, **kwargs)
        self._protocol = self._driver_setup.get('protocol', 'legacy')

        return

    @property
    def slot_id(self):
        return self._slot_id

    @property
    def group_id(self):
        return self._group_id

    @property
    def driver_setup(self):
        return self._driver_setup
    
    def _load_identity(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            card_type = self._card_type_query(self.slot_id) 
            #print('   found: {}'.format(card_type))            
            self._identity_instrument_model = card_type
            
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')

        return


class Agilent34xx_Swtch(swtch.Base):
    ''' Placeholder for inter-card routing'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return

    def _init_channels(self):
        '''load and initialize channels after driver fully built and initialized '''
        print('initializing cards and channels')
        # self._load_cards()    # discover installed cards
        # self._load_channels() # build database of possible connection endpoints
        return

    # def _load_cards(self):
    #     print('enter load_cards()')

    #     # perhaps _slots might cause confusion with pythons __slots__.
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

    def _load_channels(self):
        super()._init_channels()

        self._channel_name = list()
        self._channel_label = list()

        self.channels._set_list(self._channel_name)

        return

    def parse_channel_address(self, address_string):
        ''' splits a native hp34xx address into its slot and channel parts'''

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

        # print('checking path {}.{} -> {}.{}'.format(slot_a, chan_a, slot_b, chan_b))
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


class Agilent34xx(Agilent34xx_Driver): #, Agilent34xx_Swtch
    "Agilent HP3488 Switch driver"

    def __init__(self, *args, **kwargs):
        # hide a definition of supported models from ivi
        self.__dict__.setdefault('_driver_supported_models', ['HP3488A','HP3488B','HP3488R'])
        self._resource_string = args[0]
        
        self._protocol = None
        super().__init__(*args, **kwargs)

        print(' configuring instrument')
        
        self._instrument_id = 'HP3488'
        self._identity_description = "Agilent HP3488/HP3499 series Switch/Control Unit"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._identity_supported_instrument_models = self._driver_supported_models

        self._load_identity()
        #self._init_channels()

        return

    def _load_identity(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._rack_id().split(',')
            #print('   found: {}'.format(lst))
            
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

        return
    
    def _utility_disable(self):
        pass

    def _utility_lock_object(self):
        pass

    def _utility_unlock_object(self):
        pass

    def _utility_error_query(self):
        error_code = self._rack_error()
        error_message = 'no message'

        return (error_code, error_message)

    def _utility_reset(self):
        self._rack_reset()
        self.driver_operation.invalidate_all_attributes()

        return

    def _utility_reset_with_defaults(self):
        self._utility_reset()

        return

    def _utility_self_test(self):
        message = "Self test passed"
        code = self._rack_test()
        if code != 0:
            message = "Self test failed"

        return (code, message)


class Agilent3488(Agilent34xx):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._protocol = 'legacy'
        return


class Agilent3499(Agilent34xx):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._protocol = 'scpi'
            return
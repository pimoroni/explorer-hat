"""Cap-touch Driver Library for Microchip CAP1xxx ICs
Supports communication over i2c only.

Currently supported ICs:
CAP1208 - 8 Inputs
CAP1188 - 8 Inputs, 8 LEDs
"""
try:
    from smbus import SMBus
except ImportError:
    exit("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")

import time, signal, atexit, sys, threading

# DEVICE MAP
DEFAULT_ADDR = 0x28

# Supported devices
PID_CAP1208 = 0b01101011
PID_CAP1188 = 0b01010000

# REGISTER MAP

R_MAIN_CONTROL      = 0x00
R_GENERAL_STATUS    = 0x02
R_INPUT_STATUS      = 0x03
R_LED_STATUS        = 0x04
R_NOISE_FLAG_STATUS = 0x0A

# Read-only delta counts for all inputs
R_INPUT_1_DELTA   = 0x10
R_INPUT_2_DELTA   = 0x11
R_INPUT_3_DELTA   = 0x12
R_INPUT_4_DELTA   = 0x13
R_INPUT_5_DELTA   = 0x14
R_INPUT_6_DELTA   = 0x15
R_INPUT_7_DELTA   = 0x16
R_INPUT_8_DELTA   = 0x17

R_SENSITIVITY     = 0x1F

R_GENERAL_CONFIG  = 0x20
R_INPUT_ENABLE    = 0x21

R_INPUT_CONFIG    = 0x22

R_INPUT_CONFIG2   = 0x23 # Default 0x00000111

# Values for bits 3 to 0 of R_INPUT_CONFIG2
# Determines minimum amount of time before
# a "press and hold" event is detected.

# Also - Values for bits 3 to 0 of R_INPUT_CONFIG
# Determines rate at which interrupt will repeat
#
# Resolution of 35ms, max = 35 + (35 * 0b1111) = 560ms

R_SAMPLING_CONFIG = 0x24 # Default 0x00111001
R_CALIBRATION     = 0x26 # Default 0b00000000
R_INTERRUPT_EN    = 0x27 # Default 0b11111111
R_REPEAT_EN       = 0x28 # Default 0b11111111
R_MTOUCH_CONFIG   = 0x2A # Default 0b11111111
R_MTOUCH_PAT_CONF = 0x2B
R_MTOUCH_PATTERN  = 0x2D
R_COUNT_O_LIMIT   = 0x2E
R_RECALIBRATION   = 0x2F

# R/W Touch detection thresholds for inputs
R_INPUT_1_THRESH  = 0x30
R_INPUT_2_THRESH  = 0x31
R_INPUT_3_THRESH  = 0x32
R_INPUT_4_THRESH  = 0x33
R_INPUT_4_THRESH  = 0x34
R_INPUT_6_THRESH  = 0x35
R_INPUT_7_THRESH  = 0x36
R_INPUT_8_THRESH  = 0x37

# R/W Noise threshold for all inputs
R_NOISE_THRESH    = 0x38

# R/W Standby and Config Registers
R_STANDBY_CHANNEL = 0x40
R_STANDBY_CONFIG  = 0x41
R_STANDBY_SENS    = 0x42
R_STANDBY_THRESH  = 0x43
R_CONFIGURATION2  = 0x44

# Read-only reference counts for sensor inputs
R_INPUT_1_BCOUNT  = 0x50
R_INPUT_2_BCOUNT  = 0x51
R_INPUT_3_BCOUNT  = 0x52
R_INPUT_4_BCOUNT  = 0x53
R_INPUT_5_BCOUNT  = 0x54
R_INPUT_6_BCOUNT  = 0x55
R_INPUT_7_BCOUNT  = 0x56
R_INPUT_8_BCOUNT  = 0x57

# LED Controls - For CAP1188 and similar
R_LED_OUTPUT_TYPE = 0x71
R_LED_LINKING     = 0x72
R_LED_POLARITY    = 0x73
R_LED_OUTPUT_CON  = 0x74
R_LED_LTRANS_CON  = 0x77
R_LED_MIRROR_CON  = 0x79

# LED Behaviour
R_LED_BEHAVIOUR_1 = 0x81 # For LEDs 1-4
R_LED_BEHAVIOUR_2 = 0x82 # For LEDs 5-8
R_LED_PULSE_1_PER = 0x84
R_LED_PULSE_2_PER = 0x85
R_LED_BREATHE_PER = 0x86
R_LED_CONFIG      = 0x88
R_LED_PULSE_1_DUT = 0x90
R_LED_PULSE_2_DUT = 0x91
R_LED_BREATHE_DUT = 0x92
R_LED_DIRECT_DUT  = 0x93
R_LED_DIRECT_RAMP = 0x94
R_LED_OFF_DELAY   = 0x95

# R/W Power buttonc ontrol
R_POWER_BUTTON    = 0x60
R_POW_BUTTON_CONF = 0x61

# Read-only upper 8-bit calibration values for sensors
R_INPUT_1_CALIB   = 0xB1
R_INPUT_2_CALIB   = 0xB2
R_INPUT_3_CALIB   = 0xB3
R_INPUT_4_CALIB   = 0xB4
R_INPUT_5_CALIB   = 0xB5
R_INPUT_6_CALIB   = 0xB6
R_INPUT_7_CALIB   = 0xB7
R_INPUT_8_CALIB   = 0xB8

# Read-only 2 LSBs for each sensor input
R_INPUT_CAL_LSB1  = 0xB9
R_INPUT_CAL_LSB2  = 0xBA

# Product ID Registers
R_PRODUCT_ID      = 0xFD
R_MANUFACTURER_ID = 0xFE
R_REVISION        = 0xFF

## Basic stoppable thread wrapper
#
#  Adds Event for stopping the execution loop
#  and exiting cleanly.
class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.daemon = True         

    def start(self):
        if self.isAlive() == False:
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive() == True:
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()

## Basic thread wrapper class for asyncronously running functions
#
#  Basic thread wrapper class for running functions
#  asyncronously. Return False from your function
#  to abort looping.
class AsyncWorker(StoppableThread):
    def __init__(self, todo):
        StoppableThread.__init__(self)
        self.todo = todo

    def run(self):
        while self.stop_event.is_set() == False:
            if self.todo() == False:
                self.stop_event.set()
                break

class Cap1xxx():
    supported = [PID_CAP1208, PID_CAP1188]
  
    def __init__(self, i2c_addr=DEFAULT_ADDR, i2c_bus=1, on_touch=[None]*8):
        self.async_poll = None
        self.i2c_addr = i2c_addr
        self.i2c = SMBus(i2c_bus)
        self.count = 0

        self.handlers = {
            'press' :[None]*8,
            'release': [None]*8,
            'held'    : [None]*8
        }

        self.touch_handlers = on_touch
        self.last_input_status = [False]*8
        self.input_status = ['none']*8
        self.input_pressed = [False]*8
        self.repeat_enabled = 0b00000000
        self.release_enabled = 0b11111111
        
        self.product_id = self._get_product_id()

        if not self.product_id in self.supported:
            raise Exception("Product ID {} not supported!".format(self.product_id))

        # Enable all inputs with interrupt by default
        self.enable_inputs(0b11111111)
        self.enable_interrupts(0b11111111)

        # Disable repeat for all channels, but give
        # it sane defaults anyway
        self.enable_repeat(0b00000000)
        self.enable_multitouch(True)

        self.set_hold_delay(210)
        self.set_repeat_rate(210)

        atexit.register(self.stop_watching)

    def get_input_status(self):
        """Get the status of all inputs.
        Returns an array of 8 boolean values indicating
        whether an input has been triggered since the
        interrupt flag was last cleared."""
        touched = self._read_byte(R_INPUT_STATUS)
        #status = ['none'] * 8
        for x in range(8):
            if (1 << x) & touched:
                status = 'none'
                delta = self._get_twos_comp(self._read_byte(R_INPUT_1_DELTA + x))
                #print(delta)
                # We only ever want to detect PRESS events
                # If repeat is disabled, and release detect is enabled
                if delta > 50:
                    #  Touch down event
                    if self.input_status[x] in ['press','held']:
                        if self.repeat_enabled & (1 << x):
                            status = 'held'
                    if self.input_status[x] in ['none','release']:
                        if self.input_pressed[x]:
                            status = 'none'
                        else:
                            status = 'press'
                else:
                    # Touch release event
                    if self.release_enabled & (1 << x) and not self.input_status[x] == 'release':
                        status = 'release'
                    else:
                        status = 'none'
                self.input_status[x] = status
                self.input_pressed[x] = status in ['press','held','none']
            else:
                self.input_status[x] = 'none'
                self.input_pressed[x] = False
        return self.input_status

    def _get_twos_comp(self,val):
        if ( val & (1<< (8 - 1))) != 0:
            val = val - (1 << 8)
        return val
        
    def clear_interrupt(self):
        """Clear the interrupt flag, bit 0, of the
        main control register"""
        self._write_byte(R_MAIN_CONTROL, 0b00000000)

    def wait_for_interrupt(self, timeout=100):
        """Wait for, interrupt, bit 0 of the main
        control register to be set, indicating an
        input has been triggered."""
        start = self._millis()
        while True:
            status = self._read_byte(R_MAIN_CONTROL)
            if status & 1:
                return True
            if self._millis() > start + timeout:
                return False
            time.sleep(0.05)

    def on(self, channel=0, event='press', handler=None):
        self.handlers[event][channel] = handler
        self.start_watching()
        return True

    def start_watching(self):
        if self.async_poll == None:
            self.async_poll = AsyncWorker(self._poll)
            self.async_poll.start()
            return True
        return False

    def stop_watching(self):
        if not self.async_poll == None:
            self.async_poll.stop()
            self.async_poll = None
            return True
        return False

    def set_hold_delay(self, ms):
        """Set time before a press and hold is detected,
        Clamps to multiples of 35 from 35 to 560"""
        repeat_rate = self._calc_touch_rate(ms)
        input_config = self._read_byte(R_INPUT_CONFIG2)
        input_config = (input_config & ~0b1111) | repeat_rate
        self._write_byte(R_INPUT_CONFIG2, input_config)

    def set_repeat_rate(self, ms):
        """Set repeat rate in milliseconds, 
        Clamps to multiples of 35 from 35 to 560"""
        repeat_rate = self._calc_touch_rate(ms)
        input_config = self._read_byte(R_INPUT_CONFIG)
        input_config = (input_config & ~0b1111) | repeat_rate
        self._write_byte(R_INPUT_CONFIG, input_config)

    def _calc_touch_rate(self, ms):
        ms = min(max(ms,0),560)
        scale = int((round(ms / 35.0) * 35) - 35) / 35
        return scale

    def _poll(self):
        """Single polling pass, should be called in
        a loop, preferably threaded."""
        self.count += 1        
        if self.wait_for_interrupt():
            inputs = self.get_input_status()
            for x in range(8):
                self._trigger_handler(x, inputs[x])
            self.clear_interrupt()
        
            if self.count > 10:    
                # Force recalibration on fruit pads
                self._write_byte(0x26, 0b00001111)
                self.count = 0

    def _trigger_handler(self, channel, event):
        if event == 'none':
            return
        if callable(self.handlers[event][channel]):
            self.handlers[event][channel](channel, event)

    def _get_product_id(self):
        return self._read_byte(R_PRODUCT_ID)

    def enable_multitouch(self, en=True):
        """Toggles multi-touch by toggling the multi-touch
        block bit in the config register"""
        ret_mt = self._read_byte(R_MTOUCH_CONFIG)
        if en:
            self._write_byte(R_MTOUCH_CONFIG, ret_mt & ~0x80)
        else:
            self._write_byte(R_MTOUCH_CONFIG, ret_mt | 0x80 )

    def enable_repeat(self, inputs):
        self.repeat_enabled = inputs
        self._write_byte(R_REPEAT_EN, inputs)

    def enable_interrupts(self, inputs):
        self._write_byte(R_INTERRUPT_EN, inputs)

    def enable_inputs(self, inputs):
        self._write_byte(R_INPUT_ENABLE, inputs)

    def _write_byte(self, register, value):
        self.i2c.write_byte_data(self.i2c_addr, register, value)

    def _read_byte(self, register):
        return self.i2c.read_byte_data(self.i2c_addr, register)

    def _millis(self):
        return int(round(time.time() * 1000))

    def __del__(self):
        self.stop_watching()
        

class Cap1208(Cap1xxx):
    supported = [PID_CAP1208]

class Cap1188(Cap1xxx):
    supported = [PID_CAP1188]

'''
bus.write_byte_data(ADDR, INPUT_CONFIG_REG,  0b10100000)
bus.write_byte_data(ADDR, INPUT_CONFIG_REG2, 0b00000000)
bus.write_byte_data(ADDR, MULTI_TOUCH_REG,   0b00000000)

while True:
    int = bus.read_byte_data(ADDR,0)
    if int & 1:
        touched = bus.read_byte_data(ADDR,3)
        bus.write_byte_data(ADDR,0,0)
        for id, button in buttons.iteritems():
            if touched & id:
                print(button)
                if button in leds.keys():
                    GPIO.output(leds[button], GPIO.HIGH)
            else:
                if button in leds.keys():
                    GPIO.output(leds[button], GPIO.LOW)
'''

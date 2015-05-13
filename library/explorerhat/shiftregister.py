'''Shift Register Plugin'''

class ShiftRegister:
    def __init__(self):
        self.latch = None
        self.clock = None
        self.data  = None
        pass

    def setup(self, latch, clock, data):
        self.latch = latch # eh.output.one
        self.clock = clock # eh.output.two
        self.data  = data  # eh.output.three

        self.latch.on()
        self.clock.on()
        self.data.on()

    def _latch_low(self):
        '''Turns latch pin on, pulling to GND'''
        self.latch.on()

    def _latch_high(self):
        '''Turns latch pin off, releasing to VCC'''
        self.latch.off()

    def _assert_clock(self):
        '''Sends a single clock pulse'''
        self.clock.off()
        self.clock.on()

    def shift_out(self, state):
        '''Shift out a single byte, LSB first

        First the latch is pulled low, then each bit is checked
        in turn from LSB to MSB. The bit is set to the output/data pin
        and the clock pulse asserted to clock it into the register.
        '''
        self._latch_low()
        for p in range(8):
            self.data.write((state >> p) & 1)
            self._assert_clock()
        self._latch_high()

    def toggle_pin(self, pin, state):
        '''Sets specific output to state and all others to !state

        IO logic is inverted since ExplorerHAT outputs are active low.
        '''
        self._latch_low()
        for p in range(8):
            if p == pin:
                self.data.write(not state)
            else:
                self.data.write(state)
            self._assert_clock()
        self._latch_high()

    def chase(self, delay=0.2):
        for i in range(8):
            self.toggle_pin(i, 1)
            time.sleep(delay)

    def scan(self, delay=0.2):
        for i in range(8) + range(1,7)[::-1]:
            self.toggle_pin(i, 1)
            time.sleep(delay)

    def toggle_all(self, state):
        self._latch_low()
        for p in range(8):
            self.data.write(not state)
            self._assert_clock()
        self._latch_high()

    def toggle_odd(self, state):
        self._latch_low()
        for p in range(0,8):
            if p % 2 != 0:
                self.data.write(not state)
            else:
                self.data.on()
            self._assert_clock()
        self._latch_high()

    def toggle_even(self, state):
        self._latch_low()
        for p in range(0,8):
            self.clock.on()
            if p % 2 == 0:
                self.data.write(not state)
            else:
                self.data.on()
            self._assert_clock()
        self._latch_high()

    def demo(self):
        try:
            while True:
                for i in range(5):
                    for j in range(2):
                        self.toggle_all(j)
                        time.sleep(0.1)
                for i in range(5):
                    self.chase(delay=0.1)
                for i in range(5):
                    self.toggle_odd(0)
                    self.toggle_even(1)
                    time.sleep(0.1)
                    self.toggle_even(0)
                    self.toggle_odd(1)
                    time.sleep(0.1)
                for i in range(5):
                    self.scan(delay=0.1)
        except:
            pass
        finally:
            self.toggle_all(0)

_instance = ShiftRegister()
for attr in dir(_instance):
    if not attr.startswith('_') and callable(getattr(_instance, attr)):
        locals()[attr] = getattr(_instance, attr)

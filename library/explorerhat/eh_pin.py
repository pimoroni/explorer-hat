class Pin(object):
    '''Base class representing a GPIO Pin
     
    Pin contains methods that apply to both inputs and outputs
    '''
    type = 'Pin'

    def __init__(self, gpio, pin):
        self.pin = pin
        self.last = self.read()
        self.handle_change = False
        self.handle_high = False
        self.handle_low = False
        self.gpio = gpio

    # Return a tidy list of  all "public" methods
    def __call__(self):
        return filter(lambda x: x[0] != '_', dir(self))

    def has_changed(self):
        if self.read() != self.last:
            self.last = self.read()
            return True
        return False

    def is_off(self):
        '''Returns True if pin is in LOW/OFF state'''
        return self.read() == 0

    def is_on(self):
        '''Returns True if pin is in HIGH/ON state'''
        return self.read() == 1

    def read(self):
        '''Returns HIGH or LOW value of pin'''
        return self.gpio.input(self.pin)

    def stop(self):
        return True

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    is_high = is_on
    is_low = is_off
    get = read
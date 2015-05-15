from eh_pin import Pin
import time

DEBOUNCE_TIME = 20

class Input(Pin):
    '''Class representing a GPIO input

     Input only contains methods that apply to inputs
    '''

    type = 'Input'

    def __init__(self, gpio, pin):
        self.handle_pressed = None
        self.handle_released = None
        self.handle_changed = None
        self.has_callback = False
        self.gpio = gpio
        if self.type == 'Button':
            self.gpio.setup(pin, self.gpio.IN, pull_up_down=self.gpio.PUD_DOWN)
        else:
            self.gpio.setup(pin, self.gpio.IN)
        super(Input,self).__init__(gpio,pin)

    def on_high(self, callback, bouncetime=DEBOUNCE_TIME):
        '''Attach a callback to trigger on a transition to HIGH'''
        self.handle_pressed = callback
        self._setup_callback(bouncetime)
        return True

    def _setup_callback(self, bouncetime):
        if self.has_callback:
            return False

        def handle_callback(pin):
            if self.read() == 1 and callable(self.handle_pressed):
                self.handle_pressed(self)
            elif self.read() == 0 and callable(self.handle_released):
                self.handle_released(self)
            if callable(self.handle_changed):
                self.handle_changed(self)
        self.gpio.add_event_detect(self.pin, self.gpio.BOTH, callback=handle_callback, bouncetime=bouncetime)
        self.has_callback = True
        return True

    def on_low(self, callback, bouncetime=DEBOUNCE_TIME):
        '''Attach a callback to trigger on transition to LOW'''
        self.handle_released = callback
        self._setup_callback(bouncetime)
        return True
        
    def on_changed(self, callback, bouncetime=DEBOUNCE_TIME):
        '''Attach a callback to trigger when changed'''
        self.handle_changed = callback
        self._setup_callback(bouncetime)
        return True

    def clear_events(self):
        '''Clear all attached callbacks'''
        self.handle_pressed = None
        self.handle_released = None
        self.handle_changed = None
        self.gpio.remove_event_detect(self.pin)
        self.has_callback = False

    # Alias handlers
    changed = on_changed
    pressed = on_high
    released = on_low
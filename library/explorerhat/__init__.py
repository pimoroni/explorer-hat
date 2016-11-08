"""[explorerhat]

API library for Explorer HAT and Explorer HAT Pro, Raspberry Pi add-on boards"""

import atexit
import signal
import time
from sys import exit, version_info

try:
    from smbus import SMBus
except ImportError:
    if version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")

try:
    import RPi.GPIO as GPIO
except ImportError:
    exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")

try:
    from cap1xxx import Cap1208
except ImportError:
    exit("This library requires the cap1xxx module\nInstall with: sudo pip install cap1xxx")

from .ads1015 import read_se_adc, adc_available 
from .pins import ObjectCollection, AsyncWorker, StoppableThread


__version__ = '0.4.2'

explorer_pro = False
explorer_phat = False
has_captouch = False
has_analog = False

# Assume A+, B+ and no funny business

# Onboard LEDs above 1, 2, 3, 4
LED1 = 4
LED2 = 17
LED3 = 27
LED4 = 5

# Outputs via ULN2003A
OUT1 = 6
OUT2 = 12
OUT3 = 13
OUT4 = 16

# 5v Tolerant Inputs
IN1 = 23
IN2 = 22
IN3 = 24
IN4 = 25

# Motor, via DRV8833PWP Dual H-Bridge
M1B = 19
M1F = 20
M2B = 21
M2F = 26

# Number of times to update
# pulsing LEDs per second
PULSE_FPS = 50
PULSE_FREQUENCY = 1000

DEBOUNCE_TIME = 20

CAP_PRODUCT_ID = 107


def help(topic=None):
    return _help[topic]


class Pulse(StoppableThread):
    """Basic thread wrapper class for delta-timed LED pulsing

    Pulses an LED in perfect wall-clock time
    Small delay by 1.0/FPS to prevent unnecessary workload"""
    def __init__(self, pin, time_on, time_off, transition_on, transition_off):
        StoppableThread.__init__(self)

        self._paused = False
        self.pin = pin
        self.time_on = time_on
        self.time_off = time_off
        self.transition_on = transition_on
        self.transition_off = transition_off

        self.fps = PULSE_FPS

        # Total time of transition
        self.time_start = time.time()

    def start(self):
        self.pin.frequency(PULSE_FREQUENCY)

        if self._paused:
            self.time_start = time.time()
            self._paused = False
            return

        self.time_start = time.time()
        StoppableThread.start(self)

    def pause(self):
        self._paused = True

    def run(self):
        # This loop runs at the specified "FPS" uses time.time()
        while not self.stop_event.is_set():
            if not self._paused:
                current_time = time.time() - self.time_start
                delta = current_time % (self.transition_on+self.time_on+self.transition_off+self.time_off)

                time_off = self.transition_on + self.time_on + self.transition_off
                time_on = self.transition_on + self.time_on

                if delta <= self.transition_on:
                    # Transition On Phase
                    self.pin.duty_cycle(round((100.0 / self.transition_on) * delta))

                elif time_on < delta <= time_off:
                    # Transition Off Phase
                    current_delta = delta - self.transition_on - self.time_on
                    self.pin.duty_cycle(round(100.0 - ((100.0 / self.transition_off) * current_delta)))

                elif delta > self.transition_on < delta <= time_on:
                    self.pin.duty_cycle(100)

                elif delta > time_off:
                    self.pin.duty_cycle(0)

            time.sleep(1.0/self.fps)

        self.pin.duty_cycle(0)


class Pin(object):
    """ExplorerHAT class representing a GPIO Pin

    Pin contains methods that apply to both inputs and outputs"""
    type = 'Pin'

    def __init__(self, pin):
        self.pin = pin
        self.last = self.read()
        self.handle_change = False
        self.handle_high = False
        self.handle_low = False

    # Return a tidy list of  all "public" methods
    def __call__(self):
        return filter(lambda x: x[0] != '_', dir(self))

    def has_changed(self):
        if self.read() != self.last:
            self.last = self.read()
            return True
        return False

    def is_off(self):
        return self.read() == 0

    def is_on(self):
        return self.read() == 1

    def read(self):
        return GPIO.input(self.pin)

    def stop(self):
        return True

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __del__(self):
        pass

    is_high = is_on
    is_low = is_off
    get = read


class Motor(object):
    type = 'Motor'

    def __init__(self, pin_fw, pin_bw):
        self._invert = False
        self.pin_fw = pin_fw
        self.pin_bw = pin_bw
        self._speed = 0

        GPIO.setup(self.pin_fw, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_bw, GPIO.OUT, initial=GPIO.LOW)

        self.pwm_fw = GPIO.PWM(self.pin_fw, 100)
        self.pwm_fw.start(0)

        self.pwm_bw = GPIO.PWM(self.pin_bw, 100)
        self.pwm_bw.start(0)

    def invert(self):
        self._invert = not self._invert
        self._speed = -self._speed
        self.speed(self._speed)
        return self._invert

    def forwards(self, speed=100):
        if speed > 100 or speed < 0:
            raise ValueError("Speed must be between 0 and 100")
        if self._invert:
            self.speed(-speed)
        else:
            self.speed(speed)

    def backwards(self, speed=100):
        if speed > 100 or speed < 0:
            raise ValueError("Speed must be between 0 and 100")
        if self._invert:
            self.speed(speed)
        else:
            self.speed(-speed)

    def speed(self, speed=100):
        if speed > 100 or speed < -100:
            raise ValueError("Speed must be between -100 and 100")

        self._speed = speed
        if speed > 0:
            self.pwm_bw.ChangeDutyCycle(0)
            self.pwm_fw.ChangeDutyCycle(speed)
        if speed < 0:
            self.pwm_fw.ChangeDutyCycle(0)
            self.pwm_bw.ChangeDutyCycle(abs(speed))
        if speed == 0:
            self.pwm_fw.ChangeDutyCycle(0)
            self.pwm_bw.ChangeDutyCycle(0)

        return speed

    def stop(self):
        self.speed(0)

    forward = forwards
    backward = backwards
    reverse = invert


class Input(Pin):
    """ExplorerHAT class representing a GPIO Input

    Input contains methods that apply only to inputs"""

    type = 'Input'

    def __init__(self, pin):
        self.handle_pressed = None
        self.handle_released = None
        self.handle_changed = None
        self.has_callback = False
        if self.type == 'Button':
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)

        super(Input, self).__init__(pin)

    def on_high(self, callback, bouncetime=DEBOUNCE_TIME):
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
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=handle_callback, bouncetime=bouncetime)
        self.has_callback = True
        return True

    def on_low(self, callback, bouncetime=DEBOUNCE_TIME):
        self.handle_released = callback
        self._setup_callback(bouncetime)
        return True

    def on_changed(self, callback, bouncetime=DEBOUNCE_TIME):
        self.handle_changed = callback
        self._setup_callback(bouncetime)
        return True

    def clear_events(self):
        GPIO.remove_event_detect(self.pin)
        self.has_callback = False

    # Alias handlers
    changed = on_changed
    pressed = on_high
    released = on_low


class Output(Pin):
    """ExplorerHAT class representing a GPIO Output

    Output contains methods that apply only to outputs.
    It also contains methods for pulsing, blinking LEDs or other attached devices"""
    type = 'Output'

    def __init__(self, pin):
        GPIO.setup(pin, GPIO.OUT, initial=0)
        super(Output, self).__init__(pin)
        self.gpio_pwm = GPIO.PWM(pin, PULSE_FREQUENCY)
        self.gpio_pwm.start(0)

        self.pulser = Pulse(self, 0, 0, 0, 0)
        self.blinking = False
        self.pulsing = False
        self.fading = False
        self.fader = None
        self._value = 0

    def __del__(self):
        self.gpio_pwm.stop()
        Pin.__del__(self)

    def fade(self, start, end, duration):
        """Fades an LED to a specific brightness over a specific time in seconds

        @param self Object pointer.
        @param start Starting brightness %
        @param end Ending brightness %
        @param duration Time duration ( in seconds ) of the fade"""
        self.stop()
        time_start = time.time()
        self.pwm(PULSE_FREQUENCY, start)

        def _fade():
            self.fading = True

            if time.time() - time_start >= duration:
                self.duty_cycle(end)
                self.fading = False
                return False

            current = (time.time() - time_start) / duration
            brightness = start + (float(end-start) * current)
            self.duty_cycle(round(brightness))
            time.sleep(1.0 / PULSE_FPS)

        self.fader = AsyncWorker(_fade)
        self.fader.start()
        return True

    def blink(self, on=1, off=-1):
        """Blinks an LED by working out the correct PWM frequency/duty cycle

        @param self Object pointer.
        @param on Time the LED should stay at 100%/on
        @param off Time the LED should stay at 0%/off"""

        self.stop()

        if off == -1:
            off = on

        off = float(off)
        on = float(on)

        total = off + on

        duty_cycle = 100.0 * (on/total)

        # Use pure PWM blinking, because threads are ugly
        self.frequency(1.0/total)
        self.duty_cycle(duty_cycle)
        self.blinking = True

        return True

    def pulse(self, transition_on=None, transition_off=None, time_on=None, time_off=None):
        """Pulses an LED

        @param self Object pointer.
        @param transition_on Time the transition from 0% to 100% brightness should take
        @param transition_off Time the trantition from 100% to 0% brightness should take
        @param time_on Time the LED should stay at 100% brightness
        @param time_off Time the LED should stay at 0% brightness"""

        self.stop()

        # This needs a thread to handle the fade in and out

        # Attempt to cascade parameters
        # pulse() = pulse(0.5,0.5,0.5,0.5)
        # pulse(0.5,1.0) = pulse(0.5,1.0,0.5,0.5)
        # pulse(0.5,1.0,1.0) = pulse(0.5,1.0,1.0,1.0)
        # pulse(0.5,1.0,1.0,0.5) = -

        if transition_on is None:
            transition_on = 0.5
        if transition_off is None:
            transition_off = transition_on
        if time_on is None:
            time_on = transition_on
        if time_off is None:
            time_off = transition_on

        # pulse(x,y,0,0) is basically just a regular blink
        # only fire up a thread if we really need it
        if transition_on == 0 and transition_off == 0:
            self.blink(time_on, time_off)
            self.blinking = True
        else:
            self.pulser.time_on = time_on
            self.pulser.time_off = time_off
            self.pulser.transition_on = transition_on
            self.pulser.transition_off = transition_off
            self.pulser.start()
            self.pulsing = True

        return True

    def pwm(self, freq, duty_cycle=50):
        self.gpio_pwm.ChangeDutyCycle(duty_cycle)
        self.gpio_pwm.ChangeFrequency(freq)
        #self.gpio_pwm.start(duty_cycle)
        return True

    def frequency(self, freq):
        self.gpio_pwm.ChangeFrequency(freq)
        return True

    def duty_cycle(self, duty_cycle):
        self.gpio_pwm.ChangeDutyCycle(duty_cycle)
        return True

    def stop(self):
        """Spops all animation"""
        if self.fading:
            self.fader.stop()
            self.fading = False

        if self.pulsing:
            self.pulsing = False
            self.pulser.pause()

        if self.blinking:
            self.blinking = False

        #self.gpio_pwm.stop()
        #time.sleep(0.01)
        if self._value:
            self.duty_cycle(100)
        else:
            self.duty_cycle(0)

        #GPIO.output(self.pin, self._value)

        return True

    def stop_pulse(self):
        """Stops the pulsing thread

        @param self Object pointer."""
        self.pulsing = False
        self.pulser.stop()
        self.pulser = Pulse(self, 0, 0, 0, 0)

    def brightness(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Brightness must be between 0 and 100")

        self.frequency(PULSE_FREQUENCY)
        self.duty_cycle(value)

    def write(self, value):
        if value is not True and value is not False and value is not 1 and value is not 0:
            raise ValueError("You must write a value of 1/True or 0/False")

        self.stop()
        self._value = value

        self.frequency(PULSE_FREQUENCY)

        #print("Writing {} to pin {}".format(value, self.pin))

        # GPIO.output(self.pin, value)
        if self._value:
            self.duty_cycle(100)
        else:
            self.duty_cycle(0)

        return True

    def on(self):
        """Turns an Output on
        @param self Object pointer."""
        self.write(1)
        return True

    def off(self):
        """Turns an Output off
        @param self Object pointer."""
        self.write(0)
        return True

    high = on
    low = off

    def toggle(self):
        self.stop()

        if self.read():
            self.write(0)
        else:
            self.write(1)

        return True


class Light(Output):
    """ExplorerHAT class representing an onboard LED"""

    type = 'Light'

    def __init__(self, pin):
        super(Light, self).__init__(pin)


class AnalogInput(object):
    type = 'Analog Input'

    def __init__(self, channel):
        self.channel = channel
        self._sensitivity = 0.1
        self._t_watch = None
        self.last_value = None
        self._handler = None

    def read(self):
        return read_se_adc(self.channel)

    def sensitivity(self, sensitivity):
        self._sensitivity = sensitivity

    def changed(self, handler, sensitivity=None):
        self._handler = handler
        if sensitivity is not None:
            self._sensitivity = sensitivity
        if self._t_watch is None:
            self._t_watch = AsyncWorker(self._watch)
            self._t_watch.start()

    def _watch(self):
        value = self.read()
        if self.last_value is not None and abs(value-self.last_value) > self._sensitivity:
            if callable(self._handler):
                self._handler(self, value)
        self.last_value = value
        time.sleep(0.01)


class CapTouchSettings(object):
    type = 'Cap Touch Settings'

    @staticmethod
    def enable_multitouch(en=True):
        _cap1208.enable_multitouch(en)


class CapTouchInput(object):
    type = 'Cap Touch Input'

    def __init__(self, channel, alias):
        self.alias = alias
        self._pressed = False
        self._held = False
        self.channel = channel
        self.handlers = {'press': None, 'release': None, 'held': None}
        for event in ['press', 'release', 'held']:
            _cap1208.on(channel=self.channel, event=event, handler=self._handle_state)

    def _handle_state(self, channel, event):
        if channel == self.channel:
            if event == 'press':
                self._pressed = True
            elif event == 'held':
                self._held = True
            elif event in ['release', 'none']:
                self._pressed = False
                self._held = False
            if callable(self.handlers[event]):
                self.handlers[event](self.alias, event)

    def is_pressed(self):
        return self._pressed

    def is_held(self):
        return self._held

    def pressed(self, handler):
        self.handlers['press'] = handler

    def released(self, handler):
        self.handlers['release'] = handler

    def held(self, handler):
        self.handlers['held'] = handler

running = False
workers = {}


def async_start(name, function):
    global workers
    workers[name] = AsyncWorker(function)
    workers[name].start()
    return True


def async_stop(name):
    global workers
    workers[name].stop()
    return True


def async_stop_all():
    global workers
    for worker in workers:
        print("Stopping user task: " + worker)
        workers[worker].stop()
    return True


def set_timeout(function, seconds):
    def fn_timeout():
        time.sleep(seconds)
        function()
        return False
    timeout = AsyncWorker(fn_timeout)
    timeout.start()
    return True


def pause():
    signal.pause()


def loop(callback):
    global running
    running = True
    while running:
        callback()


def stop():
    global running
    running = False
    return True


def is_explorer_pro():
    return explorer_pro

def is_explorer_phat():
    return explorer_phat

def explorerhat_exit():
    print("\nExplorer HAT exiting cleanly, please wait...")

    print("Stopping flashy things...")
    output.stop()
    input.stop()
    light.stop()
    light.stop_pulse()

    print("Stopping user tasks...")
    async_stop_all()

    print("Cleaning up...")
    GPIO.cleanup()

    print("Goodbye!")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

try:
    _cap1208 = Cap1208()
    has_captouch = True
except IOError:
    has_captouch = False

if adc_available:
    has_analog = True
else:
    has_analog = False


if has_captouch and has_analog:
    print("Explorer HAT Pro detected...")
    explorer_pro = True

elif has_captouch and not has_analog:
    print("Explorer HAT Basic detected...")

elif has_analog and not has_captouch:
    print("Explorer pHAT detected...")
    explorer_phat = True

else:
    exit("Warning, could not find Analog or Touch...\nPlease check your i2c settings!")

atexit.register(explorerhat_exit)

try:
    settings = ObjectCollection()
    settings._add(touch=CapTouchSettings())

    light = ObjectCollection()
    light._add(blue=Light(LED1))
    light._add(yellow=Light(LED2))
    light._add(red=Light(LED3))
    light._add(green=Light(LED4))
    light._alias(amber='yellow')

    output = ObjectCollection()
    output._add(one=Output(OUT1))
    output._add(two=Output(OUT2))
    output._add(three=Output(OUT3))
    output._add(four=Output(OUT4))

    input = ObjectCollection()
    input._add(one=Input(IN1))
    input._add(two=Input(IN2))
    input._add(three=Input(IN3))
    input._add(four=Input(IN4))


    touch = ObjectCollection()
    if has_captouch:
        touch._add(one=CapTouchInput(4, 1))
        touch._add(two=CapTouchInput(5, 2))
        touch._add(three=CapTouchInput(6, 3))
        touch._add(four=CapTouchInput(7, 4))
        touch._add(five=CapTouchInput(0, 5))
        touch._add(six=CapTouchInput(1, 6))
        touch._add(seven=CapTouchInput(2, 7))
        touch._add(eight=CapTouchInput(3, 8))

# Check for the existence of the ADC
# to determine if we're running Pro

    analog = ObjectCollection()
    motor = ObjectCollection()
    if is_explorer_pro() or is_explorer_phat():
        motor._add(one=Motor(M1F, M1B))
        motor._add(two=Motor(M2F, M2B))

    if has_analog:
        analog._add(one=AnalogInput(3))
        analog._add(two=AnalogInput(2))
        analog._add(three=AnalogInput(1))
        analog._add(four=AnalogInput(0))
except RuntimeError:
    print("YOu must be root to use Explorer HAT!")
    ready = False


_help = {
    'index': '''Call with "explorerhat.help(topic)" for help with:

    * touch
    * input
    * output
    * light
    * analog
    * motor

Explorer HAT uses simple named collections of things to get you
started writing Python to control and sense the world around you.

In the same way as you called help, try calling the name of a
collection of things.

    explorerhat.touch
    ...
    explorerhat.light

You can then call methods on either entire collections, like so:

    explorerhat.light.on()

Or just one thing, like so:

    explorerhat.light.red.on()
''',
    'touch':  '''Touch Inputs

Explorer HAT includes 8 touch inputs which act just like buttons.

The 8 touch pads are named "one" to "eight" and can be called like so:

    explorerhat.touch.one
    explorerhat.touch.two
    ...
    explorerhat.touch.eight
''',
    'input':  '''Inputs

Explorer HAT includes 4 buffered, 5v tolerant inputs.

The 4 inputs are named "one" to "four" and can be called like so:

    explorerhat.input.one
    ...
    explorerhat.input.four
''',
    'output': '''Outputs

Explorer HAT includes 4 5v tolerant outputs.

Beware, these are driven through a Darlington Array ( ULN2003A )
and will *pull down to ground* rather than supply 5v.

The 4 outputs are named "one" to "four" and can be called like so:

    explorerhat.output.one
    ...
    explorerhat.output.four
''',
    'light':  '''Lights

Explorer HAT includs 4 LEDs; Yellow, Blue, Red and Green

You can call them like so:

    explorerhat.light.yellow
    ...
    explorerhat.light.green

''',
    'analog': '''Analog Inputs

Explorer HAT inclues 4, 5v tolerant analogue inputs.

The 4 analog inputs are named "one" to "four" and can be called like so:

    explorerhat.analog.one
    ...
    explorerhat.analog.four
''',
    'motor':  '''Motor Driver

Explorer HAT includes a motor driver, capable of driving two motors.

The two motors are named "one" and "two" and can be called like so:

    explorerhat.motor.one
    explorerhat.motor.two
''',
}


def help(topic='index'):
    if topic.lower() in _help.keys():
        print("HELP{}\n\n{}\n{}".format('-'*66, _help[topic.lower()], '-'*70))
    else:
        print(_help['index'])
    return None

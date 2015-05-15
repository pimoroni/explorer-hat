from eh_pin import Pin
import time
from eh_common import AsyncWorker, StoppableThread

# Number of times to udpate
# pulsing LEDs per second
PULSE_FPS = 50
PULSE_FREQUENCY = 100

class Pulse(StoppableThread):
    '''Thread wrapper class for delta-timed LED pulsing

    Pulses an LED to wall-clock time.
    '''
    def __init__(self,pin,time_on,time_off,transition_on,transition_off):
        StoppableThread.__init__(self)

        self.pin = pin
        self.time_on = (time_on)
        self.time_off = (time_off)
        self.transition_on = (transition_on)
        self.transition_off = (transition_off)

        self.fps = PULSE_FPS

        # Total time of transition
        self.time_start = time.time()

    def start(self):
        self.time_start = time.time()
        StoppableThread.start(self)

    def run(self):
        while self.stop_event.is_set() == False:
            current_time = time.time() - self.time_start
            delta = current_time % (self.transition_on+self.time_on+self.transition_off+self.time_off)

            if( delta <= self.transition_on ):
                # Transition On Phase
                self.pin.duty_cycle( round(( 100.0 / self.transition_on ) * delta) )

            elif( delta > self.transition_on + self.time_on and delta <= self.transition_on + self.time_on + self.transition_off ):
                # Transition Off Phase
                current_delta = delta - self.transition_on - self.time_on
                self.pin.duty_cycle( round(100.0 - ( ( 100.0 / self.transition_off ) * current_delta )) )

            elif( delta > self.transition_on and delta <= self.transition_on + self.time_on ):
                self.pin.duty_cycle( 100 )

            elif( delta > self.transition_on + self.time_on + self.transition_off ):
                self.pin.duty_cycle( 0 )

            time.sleep(1.0/self.fps)

        self.pin.duty_cycle( 0 )

class Output(Pin):
    '''Class representing a GPIO Output

    ONly contains methods that apply to outputs, including those for puling
    LEDs or other attached devices.
    '''
    type = 'Output'

    def __init__(self, gpio, pin):
        self.gpio = gpio
        self.gpio.setup(pin, self.gpio.OUT, initial=0)
        super(Output,self).__init__(gpio, pin)
        self.gpio_pwm = self.gpio.PWM(pin,1)

        self.pulser = Pulse(self,0,0,0,0)
        self.blinking = False
        self.pulsing = False
        self.fader = None

    def fade(self,start,end,duration):
        '''Fades an LED to a specific brightness over time

        Arguments:
        * start - Starting brightness, 0 to 255
        * end - Ending brightness, 0 to 255
        * duration - Duration in seconds
        '''
        self.stop()
        time_start = time.time()
        self.pwm(PULSE_FREQUENCY,start)
        def _fade():
            if time.time() - time_start >= duration:
                self.duty_cycle(end)
                return False
            
            current = (time.time() - time_start) / duration
            brightness = start + (float(end-start) * current)
            self.duty_cycle(round(brightness))
            time.sleep(0.1)
            
        self.fader = AsyncWorker(_fade)
        self.fader.start()
        return True

    def blink(self,on=1,off=-1):
        '''Blinks an LED by working out the correct PWM freq/duty

        Arguments:
        * on - On duration in seconds
        * off - Off duration in seconds
        '''
        if off == -1:
            off = on

        off = float(off)
        on = float(on)

        total = off + on

        duty_cycle = 100.0 * (on/total)

        # Stop the thread that's pulsing the LED
        if self.pulsing:
            self.stop_pulse();

        # Use pure PWM blinking, because threads are fugly
        if self.blinking:
            self.frequency(1.0/total)
            self.duty_cycle(duty_cycle)
        else:
            self.pwm(1.0/total,duty_cycle)
            self.blinking = True

        return True
    
    def pulse(self,transition_on=None,transition_off=None,time_on=None,time_off=None):
        '''Pulses an LED

        Arguments:
        * transition_on - Time in seconds that the transition from 0 to 100% brightness should take.
        * transition_off - Time in seconds that the transition from 100% to 0% brightness should take.
        * time_on - Time the LED should stay at 100% brightness
        * time_off - Time the LED should stay at 0% brightness
        '''
        # This needs a thread to handle the fade in and out

        # Attempt to cascade parameters
        # pulse() = pulse(0.5,0.5,0.5,0.5)
        # pulse(0.5,1.0) = pulse(0.5,1.0,0.5,0.5)
        # pulse(0.5,1.0,1.0) = pulse(0.5,1.0,1.0,1.0)
        # pulse(0.5,1.0,1.0,0.5) = -

        if transition_on == None:
            transition_on = 0.5
        if transition_off == None:
            transition_off = transition_on
        if time_on == None:
            time_on = transition_on
        if time_off == None:
            time_off = transition_on

        if self.blinking == False:
            self.pwm(PULSE_FREQUENCY,0.0)

        # pulse(x,y,0,0) is basically just a regular blink
        # only fire up a thread if we really need it
        if transition_on == 0 and transition_off == 0:
            self.blink(time_on,time_off)
        else:
            self.pulser.time_on = time_on
            self.pulser.time_off = time_off
            self.pulser.transition_on = transition_on
            self.pulser.transition_off = transition_off
            self.pulser.start()
            self.pulsing = True

        self.blinking = True

        return True

    def pwm(self,freq,duty_cycle = 50):
        '''Sets specified PWM Freq/Duty on a pin

        Arguments:
        * freq - Frequency in hz
        * duty_cycle - Value from 0 to 100
        '''
        self.gpio_pwm.ChangeDutyCycle(duty_cycle)
        self.gpio_pwm.ChangeFrequency(freq)
        self.gpio_pwm.start(duty_cycle)
        return True

    def frequency(self,freq):
        '''Change the PWM frequency'''
        self.gpio_pwm.ChangeFrequency(freq)
        return True

    def duty_cycle(self,duty_cycle):
        '''Change the PWM duty cycle'''
        self.gpio_pwm.ChangeDutyCycle(duty_cycle)
        return True

    def stop(self):
        '''Stop any running pulsing/blinking'''
        if self.fader != None:
            self.fader.stop()

        self.blinking = False
        self.stop_pulse()

        # Abruptly stopping PWM is a bad idea
        # unless we're writing a 1 or 0
        # So don't inherit the parent classes
        # stop() since weird bugs happen

        # Threaded PWM access was aborting with
        # no errors when stop coincided with a
        # duty cycle change.
        return True

    def stop_pulse(self):
        self.pulsing = False
        self.pulser.stop()
        self.pulser = Pulse(self,0,0,0,0)

    def write(self,value):
        '''Write a specific value to the output
          
        Arguments:
        * value - Should be 0 or 1 for LOW/HIGH respectively
        '''
        blinking = self.blinking

        self.stop()

        self.duty_cycle(100)
        self.gpio_pwm.stop()

        # Some gymnastics here to fix a bug ( in RPi.GPIO?)
        # That occurs when trying to output(1) immediately
        # after stopping the PWM

        # A small delay is needed. Ugly, but it works
        if blinking and value == 1:
            time.sleep(0.02)

        self.gpio.output(self.pin,value)

        return True

    def on(self):
        '''Writes the value 1/HIGH/ON to the Output'''
        self.write(1)
        return True
    
    def off(self):
        '''Writes the value 0/LOW/OFF to the Output'''
        self.write(0)
        return True

    high = on
    low  = off

    def toggle(self):
        if( self.blinking ):
            self.write(0)
            return True

        if( self.read() == 1 ):
            self.write(0)
        else:
            self.write(1)
        return True

class Light(Output):
    '''Class representing an LED

    Contains methods that only apply to LEDs
    '''

    type = 'Light'

    def __init__(self,gpio,pin):
        super(Light,self).__init__(gpio,pin)
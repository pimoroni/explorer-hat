
class Motor(object):
    '''Class representing a motor driver channel

    Contains methods for driving the motor at variable speeds
    '''
    type = 'Motor'
    
    def __init__(self, gpio, pin_fw, pin_bw):
        self.pwm = None
        self.pwm_pin = None
        self._invert = False
        self.pin_fw = pin_fw
        self.pin_bw = pin_bw
        self._speed = 0
        self.gpio = gpio
        self.gpio.setup(self.pin_fw, self.gpio.OUT, initial=self.gpio.LOW)
        self.gpio.setup(self.pin_bw, self.gpio.OUT, initial=self.gpio.LOW)

    def invert(self):
        '''Inverts the motors direction'''
        self._invert = not self._invert
        self._speed = -self._speed
        self.speed(self._speed)
        return self._invert

    def forwards(self, speed=100):
        '''Drives the motor forwards at given speed

        Arguments:
        * speed - Value from 0 to 100
        '''
        if speed > 100 or speed < 0:
            raise ValueError("Speed must be between 0 and 100")
            return False
        if self._invert:
            self.speed(-speed)
        else:
            self.speed(speed)

    def backwards(self, speed=100):
        '''Drives the motor backwards at given speed

        Arguments:
        * speed - Value from 0 to 100
        '''
        if speed > 100 or speed < 0:
            raise ValueError("Speed must be between 0 and 100")
            return False 
        if self._invert:
            self.speed(speed)
        else:
            self.speed(-speed)

    def _duty_cycle(self, duty_cycle):
        if self.pwm != None:
            self.pwm.ChangeDutyCycle(duty_cycle)

    def _setup_pwm(self, pin, duty_cycle):
        if self.pwm_pin != pin:
            if self.pwm != None:
                self.pwm.stop()
                time.sleep(0.005)
            self.pwm = self.gpio.PWM(pin, 100)
            self.pwm.start(duty_cycle)
            self.pwm_pin = pin

    def speed(self, speed=100):
        '''Drives the motor at a certain speed

        Arguments:
        * speed - Value from -100 to 100. 0 is stopped..
        '''
        if speed > 100 or speed < -100:
            raise ValueError("Speed must be between -100 and 100")
            return False
        self._speed = speed
        if speed > 0:
            self.gpio.output(self.pin_bw, self.gpio.LOW)
            self._setup_pwm(self.pin_fw, speed)
            self._duty_cycle(speed)
        if speed < 0:
            self.gpio.output(self.pin_fw, self.gpio.LOW)
            self._setup_pwm(self.pin_bw, abs(speed))
            self._duty_cycle(abs(speed))
        if speed == 0:
            if self.pwm != None:
              self.pwm.stop()
              time.sleep(0.005)
            self.pwm_pin = None
            self.pwm = None
        return speed

    def stop(self):
        '''Set the speed to 0'''
        self.speed(0)

    forward = forwards
    backward = backwards
    reverse = invert
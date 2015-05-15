import sys
import atexit
from eh_common import async_stop_all,ObjectCollection
from eh_analog import AnalogInput
from eh_touch  import TouchInput, TouchSettings
from eh_input  import Input
from eh_output import Output,Light
from eh_motor  import Motor

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
IN1  = 23
IN2  = 22
IN3  = 24
IN4  = 25

# Motor, via DRV8833PWP Dual H-Bridge
M1B  = 19
M1F  = 20
M2B  = 21
M2F  = 26

adc     = None
cap1208 = None
explorer_pro = False
input   = None
touch   = None
output  = None
light   = None
settings= None
analog  = None
motor   = None

try:
    import RPi.GPIO as gpio
except IOError:
    print()

def is_explorer_pro():
    return explorer_pro

def explorerhat_exit():
    print("\nExplorer HAT exiting cleanly, please wait...")

    print("Stopping flashy things...")
    try:
        output.stop()
        input.stop()
        light.stop()
    except AttributeError:
        pass

    print("Stopping user tasks...")
    async_stop_all()

    print("Cleaning up...")
    gpio.cleanup()

    print("Goodbye!")

def explorerhat_init():
    global adc, cap1208, explorer_pro, settings, light, output, input, touch, motor, analog

    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    from captouch import Cap1208, R_SAMPLING_CONFIG, R_SENSITIVITY, R_GENERAL_CONFIG, R_CONFIGURATION2, PID_CAP1208
    cap1208 = Cap1208()
    if not cap1208._get_product_id() == PID_CAP1208:
        exit("Explorer HAT not found...\nHave you enabled i2c?")

    cap1208._write_byte(R_SAMPLING_CONFIG, 0b00001000)
    cap1208._write_byte(R_SENSITIVITY,     0b01100000)
    cap1208._write_byte(R_GENERAL_CONFIG,  0b00111000)
    cap1208._write_byte(R_CONFIGURATION2,  0b01100000)
    cap1208.set_touch_delta(10)
    
    import analog as adc
    if adc.adc_available:
        print("Explorer HAT Pro detected...")
        explorer_pro = True
    else:    
        print("Explorer HAT Basic detected...")
        print("If this is incorrect, please check your i2c settings!")
        explorer_pro = False
        adc = None

    atexit.register(explorerhat_exit)

    settings = ObjectCollection()
    settings._add(touch = TouchSettings(cap1208))

    light = ObjectCollection()
    light._add(blue   = Light(gpio,LED1))
    light._add(yellow = Light(gpio,LED2))
    light._add(red    = Light(gpio,LED3))
    light._add(green  = Light(gpio,LED4))
    light._alias(amber = 'yellow')

    output = ObjectCollection()
    output._add(one   = Output(gpio,OUT1))
    output._add(two   = Output(gpio,OUT2))
    output._add(three = Output(gpio,OUT3))
    output._add(four  = Output(gpio,OUT4))

    input = ObjectCollection()
    input._add(one   = Input(gpio,IN1))
    input._add(two   = Input(gpio,IN2))
    input._add(three = Input(gpio,IN3))
    input._add(four  = Input(gpio,IN4))

    touch = ObjectCollection()
    touch._add(one   = TouchInput(cap1208,4,1))
    touch._add(two   = TouchInput(cap1208,5,2))
    touch._add(three = TouchInput(cap1208,6,3))
    touch._add(four  = TouchInput(cap1208,7,4))
    touch._add(five  = TouchInput(cap1208,0,5))
    touch._add(six   = TouchInput(cap1208,1,6))
    touch._add(seven = TouchInput(cap1208,2,7))
    touch._add(eight = TouchInput(cap1208,3,8))

    if is_explorer_pro():
        motor  = ObjectCollection()
        motor._add(one    = Motor(gpio,M1F,M1B))
        motor._add(two    = Motor(gpio,M2F,M2B))

        analog = ObjectCollection()
        analog._add(one   = AnalogInput(adc,3))
        analog._add(two   = AnalogInput(adc,2))
        analog._add(three = AnalogInput(adc,1))
        analog._add(four  = AnalogInput(adc,0))

    return True


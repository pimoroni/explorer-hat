#!/usr/bin/env python

# File: sensor.py
# Author; James Carlson, https://github.com/jxxcarlson
# Date: Feb 21, 2016
# Derived from code by Gisky

import time

import explorerhat


print("""

This Python code is for reporting on the 
value of a variable resistor, the "sensor".

Assumptions: a Raspberry Pi with the Pimoroni
ExplorerHat Pro software and hardware.  See

  - https://shop.pimoroni.com/products/explorer-hat
  - https://github.com/pimoroni/explorer-hat

Circuit: A voltage divider, with two resistors, 
R1 (fixed) and R2 (the sensor).  Resistor R1: 
one end  connected to 5V the other to Analog 
Input 1 and resistor R2,  Resistor R2: connect
the other end to GND.

The Raspberry Pi measures the voltage drop V2
across R2.  Using Ohm's law, one computes
the resistance R2.

Posslbile sensors: 

  - a light dependent resisistor
  - two wires attached to two nails immersed
    in a glass of water or stuck into the soil
    of a potted plant.
  - etc, etc.

Extra.  Connect the positive side of  a red LED to 5V
and the negative side to a 220 Ohm resistor.  Connect
the resistor to Output 1.  Do the same with a green
LED but connect its resistor to Output 2.  The red
LED will be on when the voltage exceeds 'threshold'.
In the contrary case the green LED will be on.


Press CTRL+C to exit.
""")

R1 = 4660
V = 5.125

threshold = 2.5
delay = 0.25

while True:
    V2  = explorerhat.analog.one.read()
    V1 = V - V2
    R2 = V2*(R1/V1)
    print('  {0:5.2f} volts   {1:5.2f} ohms'.format(round(V2,2), round(R2,2)))
    if V2 > threshold:
        explorerhat.output.one.off()
        explorerhat.output.two.on()
    else:
        explorerhat.output.one.on()
        explorerhat.output.two.off()        
    time.sleep(delay)

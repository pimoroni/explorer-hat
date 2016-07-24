#!/usr/bin/env python
# Contributed by Gisky

import time

import explorerhat


print("""
This example shows how you can read the light level from an LDR connected to analog one,
and turn on the onboard LEDs to indicate the measured level.

Press CTRL+C to exit.
""")

while True:
    level = explorerhat.analog.one.read()
    for i in range(0, 4):
        if level > float(i + 1):
            explorerhat.light[i].on()
        else:
            explorerhat.light[i].off()
    print(level)
    time.sleep(0.25)

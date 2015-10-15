#!/usr/bin/env python
print("""
This basic example tests the various functions of Explorer HAT,
touching any of the buttons should output a message, lights should pulse
and analog/digital values should be read every second.

Press CTRL+C to exit.
""")

import explorerhat
import time

explorerhat.light.pulse()
explorerhat.output.pulse()
explorerhat.motor.forwards()


def ohai(channel, event):
    print("{}: {}".format(channel, event))


explorerhat.touch.pressed(ohai)
explorerhat.touch.released(ohai)

while True:
    print(explorerhat.analog.read())
    print(explorerhat.input.read())
    time.sleep(1)

explorerhat.pause()

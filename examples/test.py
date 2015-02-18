#!/usr/bin/env python

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
   time.sleep(0.5)

explorerhat.pause()

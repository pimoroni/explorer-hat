#!/usr/bin/env python

import explorerhat
import signal, time

while True:
    print("Fading in...")
    explorerhat.light.fade(0, 100, 1)
    time.sleep(2)

    print("Fasing out...")
    explorerhat.light.fade(100, 0, 1)
    time.sleep(2)

    print("Toggling lights...")
    for x in range(10):
        explorerhat.light.toggle()
        time.sleep(0.1)

    for x in range(0, 100, 10):
        print("Setting lights to {}% brightness..".format(x))
        explorerhat.light.brightness(x)
        time.sleep(0.1)

    print("Trying raw pwm...")
    explorerhat.light.pwm(10, 50)
    time.sleep(1)

    print("Pulsing lights...")
    explorerhat.light.pulse(0.2, 0.2, 0.1, 0.1)
    time.sleep(1)

    print("Turning on lights...")
    explorerhat.light.on()
    time.sleep(1)

    print("Turning off lights...")
    explorerhat.light.off()
    time.sleep(1)

    print("Blinking lights...")
    explorerhat.light.blink(0.05, 0.05)
    time.sleep(1)

    print("Stopping lights...")
    explorerhat.light.stop()
    time.sleep(1)

    print("Pulsing lights...")
    explorerhat.light.pulse(0.2, 0.2, 0.1, 0.1)
    time.sleep(1)

    print("Stopping lights...")
    explorerhat.light.stop()
    time.sleep(1)

#explorerhat.touch.pressed(lambda x,y:explorerhat.light.on())

#explorerhat.touch.released(lambda x,y:explorerhat.light.off())

#signal.pause()

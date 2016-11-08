#!/usr/bin/env python

import explorerhat


print("""
This example shows how you can toggle lights when a button is touched.

It'll also print out the values of the digital inputs when they change, try hooking up a tactile switch!

Press CTRL+C to exit.
""")


def toggle_light(channel, event):
    if channel > 4:
        return
    if event == 'press':
        explorerhat.light[channel - 1].on()
    if event == 'release':
        explorerhat.light[channel - 1].off()


explorerhat.touch.pressed(toggle_light)
explorerhat.touch.released(toggle_light)


def handle_input(pin):
    print(pin.name, pin.read())


explorerhat.input.changed(handle_input)

explorerhat.pause()

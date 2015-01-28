#!/usr/bin/env python

import explorerhat

def toggle_light(channel, event):
    if channel > 4:
        return
    if event == 'press':
        explorerhat.light[channel-1].on()
    if event == 'release':
        explorerhat.light[channel-1].off()

explorerhat.touch.pressed(toggle_light)
explorerhat.touch.released(toggle_light)

explorerhat.pause()

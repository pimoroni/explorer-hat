#!/usr/bin/env python

import signal
from sys import exit

try:
    import pygame
except ImportError:
    exit("This script requires the pygame module\nInstall with: sudo pip install pygame")

import explorerhat


print("""
This example turns your Explorer HAT into a drum kit!

Hit any touch pad to hear a drum sound.

Press CTRL+C to exit.
""")

LEDS = [4, 17, 27, 5]

samples = [
    'sounds/hit.wav',
    'sounds/thud.wav',
    'sounds/clap.wav',
    'sounds/crash.wav',
    'sounds/hat.wav',
    'sounds/smash.wav',
    'sounds/rim.wav',
    'sounds/ting.wav'
]

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sounds = []
for x in range(8):
    sounds.append(pygame.mixer.Sound(samples[x]))


def handle(ch, evt):
    if ch > 4:
        led = ch - 5
    else:
        led = ch - 1
    if evt == 'press':
        explorerhat.light[led].fade(0, 100, 0.1)
        sounds[ch - 1].play(loops=0)
        name = samples[ch - 1].replace('sounds/','').replace('.wav','')
        print("{}!".format(name.capitalize()))
    else:
        explorerhat.light[led].off()


explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

signal.pause()

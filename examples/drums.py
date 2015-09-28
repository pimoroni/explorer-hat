#!/usr/bin/env python

import signal, pygame, explorerhat

LEDS = [4,17,27,5]

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
    explorerhat.light[led].fade(0,100,0.1)
    sounds[ch-1].play(loops=0)
  else:
    explorerhat.light[led].off()

explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

signal.pause()

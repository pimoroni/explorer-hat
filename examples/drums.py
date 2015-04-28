#!/usr/bin/env python

import signal, pygame, explorerhat

LEDS = [4,17,27,5]

samples = [
'sounds/kurz/CYCdh_Kurz01-ClHat.wav',
'sounds/kurz/CYCdh_Kurz01-PdHat.wav',
'sounds/kurz/CYCdh_Kurz01-Crash01.wav',
'sounds/kurz/CYCdh_Kurz01-OpHat01.wav',
'sounds/kurz/CYCdh_Kurz01-Kick01.wav',
'sounds/kurz/CYCdh_Kurz01-Snr01.wav',
'sounds/kurz/CYCdh_Kurz01-HfHat.wav',
'sounds/kurz/CYCdh_Kurz01-Ride01.wav'
]

samples = [
'sounds/electro/CYCdh_ElecK05-Kick01.wav',
'sounds/electro/CYCdh_ElecK05-Snr01.wav',
'sounds/electro/CYCdh_ElecK05-Snr04.wav',
'sounds/electro/CYCdh_ElecK05-OpHat01.wav',
'sounds/electro/CYCdh_ElecK05-Clap01.wav',
'sounds/electro/CYCdh_ElecK05-Clap02.wav',
'sounds/electro/CYCdh_ElecK06-Clap03.wav',
'sounds/electro/CYCdh_ElecK05-ClHat01.wav'
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
    explorerhat.light[led].on()
    sounds[ch-1].play(loops=0)
  else:
    explorerhat.light[led].off()

explorerhat.touch.pressed(handle)
explorerhat.touch.released(handle)

signal.pause()

#!/usr/bin/env python
import explorerhat, signal

def handle_analog(pin, value):
  print(pin.name, value)

explorerhat.analog.one.changed(handle_analog)

signal.pause()

#!/usr/bin/env python

import time

import explorerhat


print("""
Basic example reading analog one and two every 1s.

Press CTRL+C to exit.
""")

while True:
    one = explorerhat.analog.one.read()
    two = explorerhat.analog.two.read()
    print(one, two)
    time.sleep(1.0)

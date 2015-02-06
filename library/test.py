#!/usr/bin/env python

import explorerhat, signal

explorerhat.touch.pressed(lambda x,y:explorerhat.light.on())

explorerhat.touch.released(lambda x,y:explorerhat.light.off())

signal.pause()

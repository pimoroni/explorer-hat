#!/usr/bin/env python

import explorerhat
from pdtone import PDTone
import signal, time
import random

# Start and connect to PD
tone = PDTone()
explorerhat.settings.touch.enable_multitouch(False)

# Store all the tunes here, as lists with format (note, duration)
"""
tunes = {
  'Tetris': [
('e5',0.5),
('b4',0.25),
('c5',0.25),
('d5',0.5),
  ],
  'Mario': [
('c5',0.5),
('g5',0.25),
('e5',0.25),
('a5',0.5),
('b5',0.5),
('a#5',0.25),
('a5',0.25)
  ],
  'Tune 0': [('a5',0.5),('a5',0.5),('b5',0.5),('c5',0.5)],
  'Tune 1': [('a5',1),('a#5',0.5),('d5',1)],
  'Tune 2': [('c5',0.5),('d5',0.5),('e5',0.5)],
  'Tune 3': [('a5',0.5),('a#5',0.5),('b5',0.5),('c5',0.5)]
}

tunes_keys = ['Test','Tetris','Mario','Tune 0','Tune 1','Tune 2','Tune 3']
"""

# How many attempts does a player get at each tune
player_lives = 3

# How many tunes to go through
num_tunes = 10

# Note duration of tunes, lower is harder
tune_speed = 0.6

lives = player_lives
steps = []
running = None
current_tune = None
current_tune_idx = 0 # Start at tune 0

# Keep an index of our notes, so we can loop through
# them in order for success/failure tunes
notes_keys = ['c4','c#4','d4','d#4','e4','f4','f#4','g4','g#4','a4','a#4','b4','c5','c#5','d5','d#5','e5','f5','f#5','g5','g#5','a5','a#5','b5']

# Pins for the lights/buttons
pins = [0, 1, 2, 3]

notes = {
        'c4':   (261.63,pins[0]),
        'c#4':  (277.18,pins[1]),
	'd4':   (293.66,pins[2]),
	'd#4':	(311.13,pins[3]),

	'e4':	(329.63,pins[0]),
	'f4':	(349.23,pins[1]),
	'f#4':	(369.99,pins[2]),
	'g4':	(392.00,pins[3]),
	
	'g#4':	(415.30,pins[0]),
	'a4':	(440.00,pins[1]),
	'a#4':	(466.16,pins[2]),
	'b4':	(493.88,pins[3]),

        'c5':   (261.63*2,pins[0]),
        'c#5':  (277.18*2,pins[1]),
	'd5':   (293.66*2,pins[2]),
	'd#5':	(311.13*2,pins[3]),

	'e5':	(329.63*2,pins[0]),
	'f5':	(349.23*2,pins[1]),
	'f#5':	(369.99*2,pins[2]),
	'g5':	(392.00*2,pins[3]),
	
	'g#5':	(415.30*2,pins[0]),
	'a5':	(440.00*2,pins[1]),
	'a#5':	(466.16*2,pins[2]),
	'b5':	(493.88*2,pins[3])
	}
	
tunes = {}
tunes_keys = []

for x in range(num_tunes):
  title = 'Tune ' + str(x)
  tunes[title] = []
  tunes_keys.append(title)
  for n in range(x+2):
    tunes[title].append((
      random.choice(notes_keys),
      tune_speed
    ))


def handle_button(pin, evt):
  """
  Handle a button press, add it to the list of
  steps and play the corresponding tone
  """
  print("Got press on {}".format(pin))
  global steps, current_tune, running

  if pin > 4:
    return False
  pin -= 1

  if not running:
    return False
  button = pins.index(pin)
  print("Pressed button: " + str(button))
  print("Notes: " + str(get_notes(pin)))
  steps.append(pin)
  if check_progress():
    note = tunes[current_tune][len(steps)-1]
    tone.tone(notes[note[0]][0])
    tone.power_on()
    explorerhat.light[pin].on()

def handle_release(pin, evt):
  """
  Clears the last tone/light when a button
  is released.
  """
  if pin > 4:
    return False
  pin -= 1

  explorerhat.light[pin].off()
  tone.power_off()

def get_notes(pin):
  """
  Get all notes corresponding to a particular
  button, represented by its GPIO pin number
  """
  result = []
  for key,note in notes.iteritems():
    if pin == note[1]:
      result.append(key)
  return result

def play_note((note,duration)):
  """ 
  Play a single note through our PD instance, and
  light its corresponding LED
  """
  f = notes[note][0]
  l = notes[note][1]
  explorerhat.light[l].on()
  tone.note(f,duration)
  explorerhat.light[l].off()

def check_progress():
  """
  Loop through every button the user has pressed so far
  and check they correspond to the notes in the current tune
  """
  global steps
  for idx, step in enumerate(steps):
    if not tunes[ current_tune ][ idx ][ 0 ] in get_notes(step):
      return False
  return True

while 1:

  cont = False
  def _cont(ch, evt):
    global cont
    cont = True

  explorerhat.touch.one.pressed(_cont)

  print("Touch the left key to continue...")
  explorerhat.light.yellow.pulse()

  while not cont:
    pass

  explorerhat.light.yellow.off()

  print("Get ready...")
  for x in reversed(range(3)):
    print("{}...".format(x))
    time.sleep(0.5)

  current_tune = tunes_keys[current_tune_idx]
 
  print("Playing " + current_tune + "...")

  explorerhat.touch.pressed(None)
  explorerhat.touch.released(None)

  # Play through each note in the current tune
  for note in tunes[ current_tune ]:
    play_note(note)
    time.sleep(0.1)
  tone.tone(0)

  
  steps = []
  failed = False
  running = True
 
  explorerhat.touch.pressed(handle_button)
  explorerhat.touch.released(handle_release)
 
  # Wait for the user to fail, or populate all the steps
  while check_progress() and len(steps) < len( tunes[ current_tune ] ): 
    pass
  running = False
  time.sleep(0.5)
  explorerhat.light.off()

  #  Wait until user releases all buttons
  #for pin in pins:
  #  while explorerhat.touch[4+pin].read() == 1:
  #    pass
    
  # Check if user has succeeded or failed
  if check_progress():
    print("Clever girl...")

    # Play success tone!
    for t in range(6):
      n = notes[notes_keys[len(notes_keys)-12+t]][0]
      dur = 0.125
      if t == 5:
        dur = 0.5
      tone.note(n,dur)
    tone.tone(0)
    
    # Progress to the next tune
    current_tune_idx += 1
    if current_tune_idx >= len(tunes):
      current_tune_idx = 0
      print("You've made it!")
  else:
    print("What have you done!?")
    
    # Play fail tone
    for t in range(6):
      n = notes[notes_keys[6-t]][0]
      dur = 0.125
      if t == 5:
        dur = 0.5
      tone.note(n,dur)
    tone.tone(0)

    lives -= 1
    print(str(lives) + " lives left!")
    if lives == 0:
      lives = player_lives
      print("Whoops, you ran out of lives!")
      print("But you got to tune " + str(current_tune_idx))
      current_tune_idx = 0

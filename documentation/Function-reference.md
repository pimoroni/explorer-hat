<!--
---
title: Explorer HAT Python Function Reference
handle: explorer-hat-python-function-reference
type: tutorial
summary: A comprehensive reference for Explorer HAT's Python library
author: Phil Howard
products: [explorer-hat, explorer-hat-pro]
tags: [Explorer HAT, Raspberry Pi, Python, Programming]
images: [images/tba.png]
difficulty: Beginner
-->
# Explorer HAT Function Reference

This reference details all of the available functions on Explorer HAT touch inputs, lights, inputs, outputs, analog inputs and motor driver.

The Analog inputs and Motor driver are only available on Explorer HAT Pro.

### Touch - wrong class called?

Explorer HAT includes 8 touch inputs which act just like buttons. We've fine tuned these to be really responsive, and you can easily use them for entering PIN codes, controlling a project or playing the drums.

The 8 inputs are named "one" to "eight" and can be referenced as such:

```python
explorerhat.touch.one
explorerhat.touch.two
...
explorerhat.touch.eight
```

Each input has a number of functions for both reading its state and binding events to certain conditions:

```python
explorerhat.input.is_pressed()
```

Returns True if the input is being touched.

```python
explorerhat.input.is_held()
```
Returns True if the input has been held down for some time

```python
explorerhat.input.pressed( handler_function )
```

Calls "handler_function" whenever the input is touched.

The handler function should accept two things, a channel ( the number of the button ) and an event ( whether it's pressed/released ) and look something like this:

```python
def handle(channel, event)
    print("Got {} on {}".format(event, channel))
```

An event of `press` indicates the touch pad was pressed, and an event of `release` indicates it was released.

```python
explorerhat.input.released( handler_funtion )
```

Calls "handler_function" whenever the input is released. The handler function is the same as described above.

```python
explorerhat.input.held( handler_function )
```

Calls "handler_function" repeatedly while the input is held down ( default once every 540ms )

### Input

Explorer HAT includes 4 buffered, 5v tolerant inputs. These act just like the GPIO pins on your Pi and don't require any special treatment. When you send a HIGH signal into them, you'll read a HIGH pin state ( 1 ) in Python.

* `read()` - Read the state of the input
* `has_changed()` - Returns true if the input has changed since the last read
* `on_changed( handler_function[, bounce_time ] )` - Calls "handler_function" when the input changes, debounce time ( in ms ) is optional
* `on_low( handler_function[, bounce_time ] )` - Calls "handler_function" when the input goes low ( off )
* `on_high( handler_function[, bounce_time ] )` - Calls "handler_function" when the input goes on ( high )
* `clear_events()` - Remove all handlers

Unlike analog events, you'll get an instance of the input passed to your handler function, so you can do something like this:

```python
def changed(input):
  state = input.read()
  name  = input.name
  print("Input {} changed to {}".format(name,state))
  
explorerhat.input.one.changed(changed)
```
Then, when you change the input you'll see something like:

```bash
Input one changed to 1
Input one changed to 0
```

### Output

* `on()` - Turns the output on
* `off()` - Turns the output off
* `toggle()` - Changes the output to its opposite state
* `write( boolean )` - Writing 1 or True turns the output on, writing 0 or False turns it off
* `blink( on_time, off_time )` - Turns the output on for "on_time" and then off for "off_time"
* `pulse( fade_in_time, fade_out_time, on_time, off_time )` - Same as blink, but lets you fade between on and off
* `fade( from, to, time )` - Fade from 0-100 to 0-100 brightness over a number of seconds specified by "time"
* `stop()` - Stops any running blink, fade or pulse action

### Light

There are four lights on Explorer HAT, Yellow, Blue, Red and Green. These are named as such in Python:

```python
explorerhat.light.yellow
...
explorerhat.light.green
```

Each light includes all of the functionality of an output. See above.

### Analog ( Pro Only )

* `read()` - Returns the value of the analog input in millivolts.
* `change( handler_function, sensitivity )` - Calls "handler_function" when a change greater than the threshold millivolts occurs

### Motor ( Pro Only )

* `invert()` - Reverses the direction of forwards for this motor
* `forwards( speed )` - Turns the motor "forwards" at speed ( default 100% )
* `backwards( speed )` - Turns the motor "backwards" at speed ( default 100% )
* `speed(-100 to 100)` - Moves the motor at speed, from full backwards to full forwards

# Function Reference

This reference details all of the available functions on Explorer HAT touch inputs, lights, inputs, outputs, analog inputs and motor driver.

The Analog inputs and Motor driver are only available on Explorer HAT Pro.

### Touch

Explorer HAT includes 8 touch inputs which act just like buttons.

The 8 inputs are named "one" to "eight" and can be referenced as such:

```python
explorerhat.touch.one
explorerhat.touch.two
...
explorerhat.touch.eight
```

Each input has a number of functions for both reading its state and binding events to certain conditions:

Returns True if the input is being touched.

```python
explorerhat.input.is_pressed()
```

Returns True if the input has been held down for some time

```python
explorerhat.input.is_held()
```

Calls "handler_function" whenever the input is touched

```python
explorerhat.input.pressed( handler_function )
```
Calls "handler_function" whenever the input is released

```python
explorerhat.input.released( handler_funtion )
```

Calls "handler_function" repeatedly while the input is held down ( default once every 540ms )

```python
explorerhat.input.held( handler_function )
```

**Unimplemented/TODO**

* repeat_rate() - Configure repeat rate of input(s)
* sensitivity() - Adjust the sensitivity, from touch sensitive to proximity or fruit

### Input

Explorer HAT includes 4 buffered, 5v tolerant inputs

* read() - Read the state of the input
* has_changed() - Returns true if the input has changed since the last read
* on_changed( handler_function[, bounce_time ] ) - Calls "handler_function" when the input changes, debounce time ( in ms ) is optional
* on_low( handler_function[, bounce_time ] ) - Calls "handler_function" when the input goes low ( off )
* on_high( handler_function[, bounce_time ] ) - Calls "handler_function" when the input goes on ( high )
* clear_events() - Remove all handlers

### Output

* on() - Turns the output on
* off() - Turns the output off
* toggle() - Changes the output to its opposite state
* write( boolean ) - Writing 1 or True turns the output on, writing 0 or False turns it off
* blink( on_time, off_time ) - Turns the output on for "on_time" and then off for "off_time"
* pulse( fade_in_time, fade_out_time, on_time, off_time ) - Same as blink, but lets you fade between on and off
* fade( from, to, time ) - Fade from 0-100 to 0-100 brightness over a number of seconds specified by "time"
* stop() - Stops any running blink, fade or pulse action

### Light

There are four lights on Explorer HAT, Yellow, Blue, Red and Green. These are named as such in Python:

```python
explorerhat.light.yellow
...
explorerhat.light.green
```

Each light includes all of the functionality of an output. See above.

### Analog ( Pro Only )

* read() - Returns the value of the analog input in millivolts.

**Unimplemented / TODO**

* on_change( handler_function, threshold ) - Calls "handler_function" when a change >= threshold millivolts occurs
* on_rise( handler_function, threshold ) - Same as above, but for positive changes only
* on_fall( handler_function, threshold ) - Same as above, but for negative changes only
* on_value( handler_function, value_a[, value_b] ) - Calls "handler_function" when input = value_a or optionally falls between a and b

### Motor ( Pro Only )

* reverse() - Reverses the direction of forwards for this motor
* forwards() - Turns the motor "forwards"
* backwards() - Turns the motor "backwards"

**Unimplemented / TODO**

* speed( value ) - Turns the motor at speed, range from -100 to +100 ( full reverse to full forwards )

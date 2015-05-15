_help = {
    'index': '''Call with "explorerhat.help(topic)" for help with:

    * touch
    * input
    * output
    * light
    * analog
    * motor

Explorer HAT uses simple named collections of things to get you
started writing Python to control and sense the world around you.

In the same way as you called help, try calling the name of a
collection of things.

    explorerhat.touch
    ...
    explorerhat.light

You can then call methods on either entire collections, like so:

    explorerhat.light.on()

Or just one thing, like so:

    explorerhat.light.red.on()
''',
    'touch':  '''Touch Inputs

Explorer HAT includes 8 touch inputs which act just like buttons.

The 8 touch pads are named "one" to "eight" and can be called like so:

    explorerhat.touch.one
    explorerhat.touch.two
    ...
    explorerhat.touch.eight
''',
    'input':  '''Inputs

Explorer HAT includes 4 buffered, 5v tolerant inputs.

The 4 inputs are named "one" to "four" and can be called like so:

    explorerhat.input.one
    ...
    explorerhat.input.four
''',
    'output': '''Outputs
Explorer HAT includes 4 5v tolerant outputs.
Beware, these are driven through a Darlington Array ( ULN2003A )
and will *pull down to ground* rather than supply 5v.
The 4 outputs are named "one" to "four" and can be called like so:
    explorerhat.output.one
    ...
    explorerhat.output.four
''',
    'light':  '''Lights
Explorer HAT includs 4 LEDs; Yellow, Blue, Red and Green
You can call them like so:
    
    explorerhat.light.yellow
    ...
    explorerhat.light.green
''',
    'analog': '''Analog Inputs
Explorer HAT inclues 4, 5v tolerant analogue inputs.
The 4 analog inputs are named "one" to "four" and can be called like so:
    explorerhat.analog.one
    ...
    explorerhat.analog.four
''',
    'motor':  '''Motor Driver
Explorer HAT includes a motor driver, capable of driving two motors.
The two motors are named "one" and "two" and can be called like so:
    explorerhat.motor.one
    explorerhat.motor.two
''',
}

def help(topic = 'index'):
    if topic.lower() in _help.keys():
        print("HELP{}\n\n{}\n{}".format('-'*66,_help[topic.lower()],'-'*70))
    else:
        print(_help['index'])
    return None


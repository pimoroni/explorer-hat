#!/usr/bin/env python

"""Explorer HAT Analog Inputs Introduction"""

import _tutorial_explorerhat as tutorial


tutorial.start([
    "Welcome to Explorer HAT {name}...",
    """In this tutorial we'll introduce you to Analog Inputs.

Analog Inputs allow you to turn a variable voltage
( from 0v to 5v ) that you might get from a slider into a
digital value that you can use in your code.
""",
    lambda: tutorial.wait_for_space(),
    """You're going to need an Explorer HAT Pro for this tutorial,
so make sure you've got one and its plugged onto your Pi!
""",
    lambda: tutorial.wait_for_space(),
    """Before starting, we must "import" Explorer HAT.

Remember to type:

    import explorerhat

Go for it:
""",
    lambda: tutorial.wait_for_input("import explorerhat"),
    lambda: tutorial.importme(),
    lambda: tutorial.check_for_pro(),
    """Great! Your Explorer HAT Pro looks like it's plugged in
and ready to go. Let's start reading some analog values.

You should have a little blue Rotary Potentiometer wired up
to Analog 1 on your Explorer HAT Pro breadboard!
""",
    lambda: tutorial.wait_for_space(),
    """Now to read the analog value you'll need to use:

    explorerhat.analog.one.read()

Try it:
""",
    lambda: tutorial.wait_for_input("explorerhat.analog.one.read()"),
    lambda: tutorial.print_value("Analog One", tutorial.explorerhat.analog.one.read()),
    """Now turn the potentiometer slightly and try again:

    explorerhat.analog.one.read()
""",
    lambda: tutorial.wait_for_input("explorerhat.analog.one.read()"),
    lambda: tutorial.print_value("Analog One", tutorial.explorerhat.analog.one.read()),
    """If everything went to plan you should see a different value.

Getting an analog value into your Python code is that simple,
now you can use it to control motors, adjust the brightness of
LEDs or whatever you can imagine!

That's all for now, press space to exit!""",
    lambda: tutorial.wait_for_space(),
])

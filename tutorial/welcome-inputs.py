#!/usr/bin/env python

"""Explorer HAT Analog Inputs Introduction"""

import _tutorial_explorerhat as tutorial

tutorial.start([
    "Welcome to Explorer HAT {name}...",
    """In this tutorial we'll introduce you to Digital Inputs.

Digital inputs take a high (5V) or low (0V) voltage
and turn it into a value you can use in your code.
""",
    lambda: tutorial.wait_for_space(),
    """Before starting, we must "import" Explorer HAT.

Remember to type:

    import explorerhat

Go for it:
""",
    lambda: tutorial.wait_for_input("import explorerhat"),
    lambda: tutorial.importme(),
    """Great! Your Explorer HAT looks like it's plugged in
and ready to go. Let's start reading some digital values.

The easiest way to input a digital value is with a male to
male jump wire. Make sure you've got one handy!
""",
    lambda: tutorial.wait_for_space(),
    """Now to read a digital value you'll need to use:

    explorerhat.input.one.read()

Try it:
""",
    lambda: tutorial.wait_for_input("explorerhat.input.one.read()"),
    lambda: tutorial.print_value("Input One", tutorial.explorerhat.input.one.read()),
    """Now, use your jump wire to connect input one to 5V.

And ready the input again:

    explorerhat.input.one.read()
""",
    lambda: tutorial.wait_for_input("explorerhat.input.one.read()"),
    lambda: tutorial.print_value("Input One", tutorial.explorerhat.input.one.read()),
    """If everything went to plan you should see a different value.

Getting a digital value into your Python code is that simple,
now you can add all the tactile buttons you could ever need!

That's all for now, press space to exit!""",
    lambda: tutorial.wait_for_space(),
])

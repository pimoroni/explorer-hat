#!/usr/bin/env python

"""Explorer HAT Introduction"""

import _tutorial_explorerhat as tutorial

tutorial.start([
    "Welcome to Explorer HAT {name}...",
    """In this introduction, we'll show you the basics.

    You'll learn how to turn a light on and off,
    and how to use a fancy pulse effect too!
    """,
    lambda: tutorial.wait_for_space(),
    """Before starting, we must "import" Explorer HAT.

    This loads the Python code, called a module, needed
    to make Explorer HAT work.

    To do this, type:

        import explorerhat

    Try it now:""",
    lambda: tutorial.wait_for_input("import explorerhat"),
    lambda: tutorial.importme(),
    """You can do this when you run "python" on the command
    line, and also in IDLE.

    Now, let's learn a little about Explorer HAT. It has:

    * 4 inputs, which accept up to 5 volts
    * 4 outputs, which sink up to 5 volts to ground
    * 4 LEDs; Yellow, Red, Blue and Green
    * 8 touch inputs, 4 are fruit compatible

    If you have an Explorer HAT Pro, you'll also find:

    * 2 Motor outputs, for making robots!
    * 4 Analog Inputs for reading sensors, sliders and stuff
    """,
    """Let's start with something simple. We'll turn on an LED.

    Type:

        explorerhat.light.red.on()
    """,
    lambda: tutorial.wait_for_input("explorerhat.light.red.on()"),
    lambda: tutorial.explorerhat.light.red.on(),
    """Neat, huh? But what if we want to turn on ALL THE LEDS!!!

    Try:

        explorerhat.light.on()
    """,
    lambda: tutorial.wait_for_input("explorerhat.light.on()"),
    lambda: tutorial.explorerhat.light.on(),
    """Easy!

    Well, {name}. You'll be happy to know Explorer HAT
    really doesn't get much harder than this.

    Everything is in a collection, like "led" or "input".

    You refer to things by using the collection name, IE:

        explorerhat.light

    Or an item in a collection by referring to it by name, IE:

        explorerhat.light.red

    So, let's turn our lights off and try something more exciting.

    Type:

        explorerhat.light.off()
    """,
    lambda: tutorial.wait_for_input("explorerhat.light.off()"),
    lambda: tutorial.explorerhat.light.off(),
    """Boom! Now let's make 'em pulse! Aww yeah!

    Type:

        explorerhat.light.pulse()
    """,
    lambda: tutorial.wait_for_input("explorerhat.light.pulse()"),
    lambda: tutorial.explorerhat.light.pulse(),
    """Excellent! Well done {name}, you've mastered the basics.

    One last thing...

    Any time you need a helping hand, just type:

        explorerhat.help()

    """
])

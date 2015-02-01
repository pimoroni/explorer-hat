#!/usr/bin/env python

'''Explorer HAT Introduction'''

import time, sys
explorerhat = None

DEFAULT_PAUSE = 0.5
DEFAULT_DELAY = 0.02

name = ''

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
 
char = None


horse = '''
     >>\.
    /_  )`.
   /  _)`^)`.   _.---. _
  (_,' \  `^-)""      `.\\
        |              | \\
        \              / |
       / \  /.___.'\  (\ (_
      < ,"||     \ |`. \`-'
       \\\\ ()      )|  )/
hjw    |_>|>     /_] //
         /_]        /_]'''
 
def keypress():
    return getch()

def importme():
    global explorerhat
    try:
        import explorerhat
    except ImportError:
        output(horse)
        typewrite("\nWoah! Hold your horses, you've not installed the library!")
        time.sleep(0.2)
        typewrite("\nI'm going to send you back to the command line where you should type:")
        time.sleep(0.2)
        typewrite("\nsudo pip install explorerhat")
        time.sleep(0.2)
        typewrite("\nGot it?")
        waitforspace()
        exit()

def output(string):
    for char in string:
        sys.stdout.write(char)
    sys.stdout.flush()

def waitforinput(string):
    output("\n>>> ")
    #waitfor(string, True)
    while True:
        if string == getinput():
            return True
        else:
            typewrite("Whoops! That isn't quite right. Try again!")
            typewrite(">>> ")

def getinput():
    try:
        string = raw_input()
    except NameError:
        string = input()
    return string

def waitfor(string, echo = True, pause = DEFAULT_PAUSE):
    for char in string:
        while keypress() != char:
            pass
        if echo:
            output(char)
    time.sleep(pause)

def waitforspace():
    typewrite('Press <space> to continue...')
    waitfor(' ', False, 0.1)

def typewrite(string, delay = DEFAULT_DELAY):
    output("\n")
    time.sleep(delay)
    for char in string:
        output(char)
        time.sleep(delay)

def getname():
    global name
    typewrite("Hi! Who are you?\n")
    name = getinput()
    output("\n")

welcome = [
    lambda:getname(),
    'Welcome to Explorer HAT {name}...',
    '',
    '''In this introduction, we'll show you the absolute basics
you will need to get Explorer HAT up and running.

We'll teach you how to turn on and off a light, and
how to get help when you need it.

Are you ready?''',
    lambda:waitforspace(),
    '''
Okay! Great...
''',
    '''
Before starting, we must import the Explorer HAT library.

To do this, type: "import explorerhat"

This works when you use "python" on the command line,
or if you're running IDLE.

Try it now:''',
    lambda:waitforinput('import explorerhat'),
    lambda:importme(),
    '''
Great! Now we can continue...
''',
    '''
But first, we need to learn a little about how Explorer HAT works.

* It has 4 inputs, which wont break if you feed them 5 volts.
* It has 4 outputs, which will sink either 3.3 or 5 volts to ground.
* It has 4 LEDs; Yellow, Red, Blue and Green
* And it has a whopping 8 capacitive touch inputs, 4 of which are fruit compatible.

If you're lucky enough to have an Explorer HAT Pro, you'll also find:

* 2 Motor outputs, for making robots!
* 4 Analog Inputs for reading sensors, sliders and potentiometers

''',
    '''
Let's start with something simple. We'll turn on an LED.

Type: "explorerhat.light.red.on()"
''',
    lambda:waitforinput('explorerhat.light.red.on()'),
    lambda:explorerhat.light.red.on(),
    '''
Neat, huh? But what if we want to turn on ALL THE LEDS!!!

Try: "explorerhat.light.on()"
''',
    lambda:waitforinput('explorerhat.light.on()'),
    lambda:explorerhat.light.on(),
'''
Easy!

Well, I've got news for you. Explorer HAT really doesn't get much harder
than this. Everything is in a collection, like "led", "input" or "output".

You refer to everything in a collection by just using the collection name, IE:

explorerhat.light

Or one item in a collection by referring to it specifically, IE:

explorerhat.light.red

So, let's turn our lights off and try something more exciting.

Type: explorerhat.light.off()
''',
    lambda:waitforinput('explorerhat.light.off()'),
    lambda:explorerhat.light.off(),
'''
Boom! Now let's make 'em pulse! Aww yeah!

Type: explorerhat.light.pulse()
''',
    lambda:waitforinput('explorerhat.light.pulse()'),
    lambda:explorerhat.light.pulse(),
'''
Excellent! You've mastered the basics.

There's nothing more to learn here, we'll drop you to the
command line and you can run the next tutorial with:

sudo ./outputs.py
''',
    lambda:waitforspace(),
]

for msg in welcome:
    if callable(msg):
        msg()
    else:
        typewrite(msg.replace('{name}',name))
        time.sleep(0.2)

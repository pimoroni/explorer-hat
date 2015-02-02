#!/usr/bin/env python

'''Explorer HAT Introduction'''

import time, sys, colorama, atexit
explorerhat = None

DEFAULT_PAUSE = 0.5
DEFAULT_DELAY = 0.02

name = ''

def exit_handler():
    print(colorama.Fore.RESET + colorama.Back.RESET)

atexit.register(exit_handler)

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
        for led in explorerhat.light
            pass
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

def prompt():
    output("\n>>> " + colorama.Fore.GREEN)

def waitforinput(string):
    prompt()
    while True:
        if string == getinput():
            return True
        else:
            typewrite(colorama.Fore.RESET + "Whoops! That isn't quite right. Try again!")
            prompt()

def getinput():
    try:
        string = raw_input()
    except NameError:
        string = input()
    output(colorama.Fore.RESET)
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
    prompt()
    name = getinput()

welcome = [
lambda:getname(),
'Welcome to Explorer HAT {name}...',
'''In this introduction, we'll show you the basics.

You'll learn how to turn a light on and off,
and how to use a fancy pulse effect too!
''',
lambda:waitforspace(),
'''Before starting, we must "import" Explorer HAT.

This loads the Python code, called a module, needed
to make Explorer HAT work.

To do this, type:

    import explorerhat

Try it now:''',
lambda:waitforinput('import explorerhat'),
lambda:importme(),
'''You can do this when you run "python" on the command 
line, and also in IDLE.

Now, let's learn a little about Explorer HAT. It has:

* 4 inputs, which accept up to 5 volts
* 4 outputs, which sink up to 5 volts to ground
* 4 LEDs; Yellow, Red, Blue and Green
* 8 touch inputs, 4 are fruit compatible

If you have an Explorer HAT Pro, you'll also find:

* 2 Motor outputs, for making robots!
* 4 Analog Inputs for reading sensors, sliders and stuff
''',
'''Let's start with something simple. We'll turn on an LED.

Type:

    explorerhat.light.red.on()
''',
lambda:waitforinput('explorerhat.light.red.on()'),
lambda:explorerhat.light.red.on(),
'''Neat, huh? But what if we want to turn on ALL THE LEDS!!!

Try:

    explorerhat.light.on()
''',
lambda:waitforinput('explorerhat.light.on()'),
lambda:explorerhat.light.on(),
'''Easy!

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
''',
lambda:waitforinput('explorerhat.light.off()'),
lambda:explorerhat.light.off(),
'''Boom! Now let's make 'em pulse! Aww yeah!

Type:

    explorerhat.light.pulse()
''',
lambda:waitforinput('explorerhat.light.pulse()'),
lambda:explorerhat.light.pulse(),
'''Excellent! Well done {name}, you've mastered the basics.

One last thing...

Any time you need a helping hand, just type:

    explorerhat.help()

Now, run the next tutorial with:

    sudo ./outputs.py
'''
]

for msg in welcome:
    if callable(msg):
        msg()
    else:
        msg = msg.replace('{name}', colorama.Fore.BLUE + name + colorama.Fore.RESET)
        msg = msg.replace('    ', colorama.Fore.GREEN + '    ')
        msg = msg.replace("\n", colorama.Fore.RESET + "\n")
        typewrite(msg)
        time.sleep(0.2)

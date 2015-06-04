#!/usr/bin/env python

'''Explorer HAT Analog Inputs Introduction'''

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
        for led in explorerhat.light:
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
    output("\n")

def typewrite(string, delay = DEFAULT_DELAY):
    output("\n")
    time.sleep(delay)
    for char in string:
        output(char)
        time.sleep(delay)

def printValue(device,val):
    typewrite('{} returned {}'.format(device, val))

def getname():
    global name
    typewrite("Hi! Who are you?\n")
    prompt()
    name = getinput()

def checkForPro():
    try:
        explorerhat.analog.one.read()
    except:
        typewrite(colorama.Fore.RED + "Uh oh! You need an Explorer HAT Pro!")
        time.sleep(1)
        exit()

welcome = [
lambda:getname(),
'Welcome to Explorer HAT {name}...',
'''In this tutorial we'll introduce you to Analog Inputs.

Analog Inputs allow you to turn a variable voltage 
( from 0v to 5v ) that you might get from a slider into a
digital value that you can use in your code.
''',
lambda:waitforspace(),
'''You're going to need an Explorer HAT Pro for this tutorial,
so make sure you've got one and its plugged onto your Pi!
''',
lambda:waitforspace(),
'''Before starting, we must "import" Explorer HAT.

Remember to type:

    import explorerhat

Go for it:
''',
lambda:waitforinput('import explorerhat'),
lambda:importme(),
lambda:checkForPro(),
'''Great! Your Explorer HAT Pro looks like it's plugged in
and ready to go. Let's start reading some analog values.

You should have a little blue Rotary Potentiometer wired up
to Analog 1 on your Explorer HAT Pro breadboard!
''',
lambda:waitforspace(),
'''Now to read the analog value you'll need to use:

    explorerhat.analog.one.read()

Try it:
''',
lambda:waitforinput('explorerhat.analog.one.read()'),
lambda:printValue('Analog One',explorerhat.analog.one.read()),
'''Now turn the potentiometer slightly and try again:

    explorerhat.analog.one.read()
''',
lambda:waitforinput('explorerhat.analog.one.read()'),
lambda:printValue('Analog One',explorerhat.analog.one.read()),
'''If everything went to plan you should see a different value.

Getting an analog value into your Python code is that simple,
now you can use it to control motors, adjust the brightness of
LEDs or whatever you can imagine!

That's all for now, press space to exit!''',
lambda:waitforspace()
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

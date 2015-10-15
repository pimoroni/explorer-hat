import time
import sys
import colorama
import atexit

try:
    from msvcrt import getch
except ImportError:
    import tty
    import termios


    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

DEFAULT_PAUSE = 0.5
DEFAULT_DELAY = 0.02


def exit_handler():
    print(colorama.Fore.RESET + colorama.Back.RESET)


def key_press():
    return getch()


def output(string):
    for char in string:
        sys.stdout.write(char)
    sys.stdout.flush()


def prompt():
    output("\n>>> " + colorama.Fore.GREEN)


def wait_for_input(string):
    prompt()
    while True:
        if string == get_input():
            return True
        else:
            type_write(colorama.Fore.RESET + "Whoops! That isn't quite right. Try again!")
            prompt()


def get_input():
    try:
        string = raw_input()
    except NameError:
        string = input()
    output(colorama.Fore.RESET)
    return string


def wait_for(string, echo=True, pause=DEFAULT_PAUSE):
    for char in string:
        while key_press() != char:
            pass
        if echo:
            output(char)
    time.sleep(pause)


def wait_for_space():
    type_write('Press <space> to continue...')
    wait_for(' ', False, 0.1)


def type_write_warning(string, delay=DEFAULT_DELAY):
    type_write(colorama.Fore.RED + string, delay)


def type_write(string, delay=DEFAULT_DELAY):
    output("\n")
    time.sleep(delay)
    for char in string:
        output(char)
        time.sleep(delay)


def add_placeholder(key, value):
    placeholders[key] = value


def print_value(device, val):
    type_write('{} returned {}'.format(device, val))


def start(messages):
    for msg in messages:
        if callable(msg):
            msg()
        else:
            for key, value in placeholders.items():
                msg = msg.replace(key, colorama.Fore.BLUE + value + colorama.Fore.RESET)

            msg = msg.replace('    ', colorama.Fore.GREEN + '    ')
            msg = msg.replace("\n", colorama.Fore.RESET + "\n")
            type_write(msg)
        time.sleep(0.2)


atexit.register(exit_handler)

placeholders = {}

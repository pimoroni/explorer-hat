from _tutorial import *


explorerhat = None

name = ''

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


def importme():
    global explorerhat
    try:
        import explorerhat
    except ImportError:
        output(horse)
        type_write("\nWoah! Hold your horses, you've not installed the library!")
        time.sleep(0.2)
        type_write("\nI'm going to send you back to the command line where you should type:")
        time.sleep(0.2)
        type_write("\nsudo pip install explorerhat")
        time.sleep(0.2)
        type_write("\nGot it?")
        wait_for_space()
        exit()


def check_for_pro():
    try:
        explorerhat.analog.one.read()
    except:
        type_write_warning("Uh oh! You need an Explorer HAT Pro!")
        time.sleep(1)
        exit()


def get_name():
    global name
    type_write("Hi! Who are you?\n")
    prompt()
    return get_input()


add_placeholder("{name}", get_name())

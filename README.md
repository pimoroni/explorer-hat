# Explorer HAT

This library is based on the Pibrella framework, you might find much of it familiar. It's got added motors, capacitive touch and analog input though!

## Pre-requisites

Explorer HAT and Explorer HAT Pro both require i2c, the easiest way to enable it is with our simple script:

```bash
curl get.pimoroni.com/i2c | bash
```

They also require the SMBus Python module, which you'll need to install like so:

```bash
sudo apt-get install python-smbus
```

## Getting Started

To get started, start up a Python interactive shell:

```bash
sudo python
```

or

```bash
sudo idle
```

...and poke Explorer HAT's innards to see what it's got to offer:

```python
import explorerhat
explorerhat.input
explorerhat.output
explorerhat.touch
explorerhat.light
```

On Explorer HAT Pro, you will also find:

```python
import explorerhat
explorerhat.analog
explorerhat.motor
```

To turn on one of the lights, address it by the name you found above:

```python
import explorerhat
explorerhat.light.red.on()
```

Or you can wait for a touch on one of the buttons:

```python
import explorerhat
def ohai(channel, event):
    print("Ohai! I got a touch on button: {}".format(channel))
explorerhat.touch.one.pressed(ohai)
```


# Documentation

* [Explorer HAT Function Reference](/REFERENCE.md)
* [Explorer HAT Pinout](/PINS.md)

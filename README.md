![Explorer HAT/pHAT](explorer-hat.png)

The Explorer HAT and Explorer HAT Pro have a heap of useful input and output options that will take your Raspberry Pi projects to the next level. Great for driving motors, using analog sensors, interfacing with 5V systems, and touch (even fruit based!) interfaces.

Learn more: https://shop.pimoroni.com/products/explorer-hat

## Installing The Library

**Full install ( recommended ):**

Just run our installer. To do this fire up Terminal which you'll find in Menu -> Accessories -> Terminal on your Raspberry Pi desktop like so:

![Finding the terminal](terminal.jpg)

In the new terminal window type:

```bash
curl -sS https://get.pimoroni.com/explorerhat | bash
```

All the pre-requisites, libraries and examples you'll need to get started will be installed for you.

If you choose to download examples you'll find them in `/home/pi/Pimoroni/explorerhat/`.

**Library install for Python 3:**

on Raspbian:

```bash
sudo apt-get install python3-explorerhat
```
other environments: 

```bash
sudo pip3 install explorerhat
```

**Library install for Python 2:**

on Raspbian:

```bash
sudo apt-get install python-explorerhat
```
other environments: 

```bash
sudo pip2 install explorerhat
```

In all cases you will have to enable the i2c bus.

## Getting Started

To get started, start up a Python 3 interactive shell:

```bash
sudo python3
```

or

```bash
sudo idle3 &
```

or Python 2:

```bash
sudo python
```

or

```bash
sudo idle &
```

...and poke Explorer HAT's innards to see what it's got to offer:

```python
import explorerhat
explorerhat.input
explorerhat.output
explorerhat.touch
explorerhat.light
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

On Explorer HAT Pro, you will also find:

```python
import explorerhat
explorerhat.analog
explorerhat.motor
```

The Explorer pHAT has most of those features except the light and touch classes, so:

```python
import explorerhat
explorerhat.input
explorerhat.output
explorerhat.analog
explorerhat.motor
```

## Notes

Explorer HAT/pHAT uses an output driver chip called the ULN2003A, which contains a set of transistor pairs called a Darlington Array. It transforms the small logic signal of the Pi into something capable of driving much bigger loads, such as motors, steppers, lights and more. 

The 4 outputs on Explorer can sink 5V, but not source. This means you need to connect your load to one of the 5V pins, and then to the output. When you turn the output on it will connect your circuit to ground, allowing current to flow and your load to turn on. This is the opposite of using a bare Pi GPIO pin, where you might connect to the pin and then to ground; keep this in mind!


# Documentation

* [Explorer HAT Function Reference](/documentation/Function-reference.md)
* [Explorer HAT Pinout](/documentation/GPIO-pins.md)
* Tutorials - https://learn.pimoroni.com/explorer-hat
* Get help - http://forums.pimoroni.com/c/support

### GPIO Pinouts

* Explorer pHAT: https://pinout.xyz/pinout/explorer_phat
* Explorer HAT: https://pinout.xyz/pinout/explorer_hat
* Explorer HAT Pro: https://pinout.xyz/pinout/explorer_hat_pro

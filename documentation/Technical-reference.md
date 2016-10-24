<!--
---
title: Explorer HAT/pHAT Technical Reference
handle: explorer-hat-technical-reference
type: technical
summary: A comprehensive technical reference for Explorer HAT/pHAT
author: Phil Howard
products: [explorer-hat, explorer-hat-pro, explorer-phat]
tags: [Explorer HAT, Raspberry Pi, Hardware]
images: [images/tba.png]
difficulty: Intermediate
-->
# Pinout

### ADC, via ADS1015, i2c addr 0x48 ( Explorer HAT Pro and pHAT only )

The Explorer HAT ADC uses i2c, so it doesn't have input pins associated with it.

### Cap Touch, via CAP1208, i2c addr 0x28

Read from register 3 to retrieve button states. These will latch until register 0 is cleared.

Register 0 will show an 0x01, interrupt, flag if a touch has been detected since the last clear.

Button | Register Value
-------|-----------------
1      | 0x10
2      | 0x20
3      | 0x40
4      | 0x80
5      | 0x1
6      | 0x2
7      | 0x4
8      | 0x8

### LEDs ( HAT only )

Both models of Explorer HAT have 4 LEDs, these are turned on with a logic HIGH and off with a LOW.

LED   | GPIO pin
------|--------
LED 1 | GPIO 4
LED 2 | GPIO 17
LED 3 | GPIO 27
LED 4 | GPIO 5

### Outputs, via ULN2003A

Explorer HAT/pHAT has a ULN2003A output driver. When you turn one of these outputs on ( logic HIGH ) it will sink current to ground. Be mindful of this when connecting to the output driver- you'll need to connect your device to a voltage supply, and then to the output pin.

Output   | GPIO pin
---------|----------
Output 1 | GPIO 6
Output 2 | GPIO 12
Output 3 | GPIO 13
Output 4 | GPIO 16

### Inputs, via SN74LVC125APWR (5V tolerant input buffer)

Explorer HAT/pHAT has four protected inputs. These are just like normal input pins on your Pi, except they can tolerate 5V.

Input    | GPIO pin
---------|-----------
Input 1  | GPIO 23
Input 2  | GPIO 22
Input 3  | GPIO 24
Input 4  | GPIO 25

### Motor, via DRV8833PWP ( Explorer HAT Pro and pHAT only )

Explorer HAT Pro has a motor driver onboard. It can drive motors in both directions depending on which pin you switch high and which you switch low. It uses two pairs of pins- 21,26 and 19,20 for each motor channel.

Function | Motor | GPIO pin
---------|-------|-----------
    +    |   1   | GPIO 19
    -    |   1   | GPIO 20
    +    |   2   | GPIO 21
    -    |   2   | GPIO 26

### 3.3v breakout ( Explorer HAT Pro only )

Explorer HAT Pro breaks out a number of your Raspberry Pi IO pins to give you convenient access to I2C, PWM, SPI and Serial/UART. None of these pins are 5V tolerant, so be careful what you connect!

Function | GPIO pin
---------|----------
SDA      | GPIO 2
SCL      | GPIO 3
---------|----------
PWM      | GPIO 18
---------|----------
MOSI     | GPIO 10
MISO     | GPIO 9
SCK      | GPIO 11
CS       | GPIO 8
---------|----------
TX       | GPIO 14
RX       | GPIO 15

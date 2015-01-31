# Pinout

### ADC, via ADS1015, i2c addr 0x48 ( Explorer HAT Pro only )

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

### LEDs

LED   | GPIO pin
------|--------
LED 1 | GPIO 4
LED 2 | GPIO 17
LED 3 | GPIO 27
LED 4 | GPIO 5

### Outputs, via ULN2003A

Output   | GPIO pin
---------|----------
Output 1 | GPIO 6
Output 2 | GPIO 12
Output 3 | GPIO 13
Output 4 | GPIO 16

### Inputs, via 5V tolerant input buffer

Input    | GPIO pin
---------|-----------
Input 1  | GPIO 23
Input 2  | GPIO 22
Input 3  | GPIO 24
Input 4  | GPIO 25

### Motor, via DRV8833PWP ( Explorer HAT Pro only )

Function | Motor | GPIO pin
---------|-------|-----------
    +    |   2   | GPIO 21
    -    |   2   | GPIO 26
    +    |   1   | GPIO 19
    -    |   1   | GPIO 20

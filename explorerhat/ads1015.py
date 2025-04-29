import time
from sys import exit, version_info

try:
    from smbus import SMBus
except ImportError:
    if version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")


adc_available = True


def i2c_bus_id():
    revision = ([l[12:-1] for l in open('/proc/cpuinfo', 'r').readlines() if l[:8] == "Revision"] + ['0000'])[0]
    return 1 if int(revision, 16) >= 4 else 0


address = 0x48
i2c = SMBus(i2c_bus_id())

REG_CONV = 0x00
REG_CFG = 0x01

samples_per_second_map = {128: 0x0000, 250: 0x0020, 490: 0x0040, 920: 0x0060, 1600: 0x0080, 2400: 0x00A0, 3300: 0x00C0}
channel_map = {0: 0x4000, 1: 0x5000, 2: 0x6000, 3: 0x7000}
programmable_gain_map = {6144: 0x0000, 4096: 0x0200, 2048: 0x0400, 1024: 0x0600, 512: 0x0800, 256: 0x0A00}

PGA_6_144V = 6144
PGA_4_096V = 4096
PGA_2_048V = 2048
PGA_1_024V = 1024
PGA_0_512V = 512
PGA_0_256V = 256


def busy():
    data = i2c.read_i2c_block_data(address, REG_CFG)
    status = (data[0] << 8) | data[1]
    return (status & (1 << 15)) == 0


def read_se_adc(channel=1):
    programmable_gain = PGA_6_144V
    samples_per_second = 250

    # sane defaults
    config = 0x0003 | 0x0100

    config |= samples_per_second_map[samples_per_second]
    config |= channel_map[channel]
    config |= programmable_gain_map[programmable_gain]

    # set "single shot" mode
    config |= 0x8000

    # write single conversion flag
    i2c.write_i2c_block_data(address, REG_CFG, [(config >> 8) & 0xFF, config & 0xFF])

    # Time the ADC conversion to disambiguate ADS1015 from ADS1115
    # Genius out of the box thinking by Niko
    # the ADS1015 will run this at 250SPS
    # the ADS1115 will run this at 16!!! SPS
    # Since the difference is ~an order of magnitude~ they're easy to tell apart.
    t_start = time.time()

    while busy():
        # We've got a lock on the I2S bus, but probably don't want to hog it!
        time.sleep(1.0 / 160)

    t_end = time.time()
    t_elapsed = t_end - t_start

    data = i2c.read_i2c_block_data(address, REG_CONV)

    if t_elapsed < 1.0 / 16: # 1/16th second is ADS1115 speed, if it's faster it must be an ADS1015
        # 12-bit
        value = (data[0] << 4) | (data[1] >> 4)

        if value & 0x800:  # Check and apply sign bit
            value -= 1 << 12

        value /= 2047.0  # Divide by full scale range

    else: # If it's slower than "ideal" ADS1115 then it's an ADS1115
        # 16-bit
        value = (data[0] << 8) | data[1]

        if value & 0x8000:  # Check and apply sign bit
            value -= 1 << 16

        value /= 32767.0  # Divide by full scale rane

    value *= float(programmable_gain)  # Multiply by gain
    value /= 1000.0  # Scale from mV to V
    value = max(0, value)  # Sweep negative voltages under the rug

    return value


try:
    read_se_adc()
except IOError:
    adc_available = False

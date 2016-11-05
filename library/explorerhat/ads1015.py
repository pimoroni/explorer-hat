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


def read_se_adc(channel=1, programmable_gain=PGA_6_144V, samples_per_second=1600):
    # sane defaults
    config = 0x0003 | 0x0100

    config |= samples_per_second_map[samples_per_second]
    config |= channel_map[channel]
    config |= programmable_gain_map[programmable_gain]

    # set "single shot" mode
    config |= 0x8000

    # write single conversion flag
    i2c.write_i2c_block_data(address, REG_CFG, [(config >> 8) & 0xFF, config & 0xFF])

    delay = (1.0 / samples_per_second) + 0.0001
    time.sleep(delay)

    data = i2c.read_i2c_block_data(address, REG_CONV)

    return (((data[0] << 8) | data[1]) >> 4) * programmable_gain / 2048.0 / 1000.0


try:
    read_se_adc()
except IOError:
    adc_available = False

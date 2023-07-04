# Welcome to the chip.fail glitcher
# This Jupyter Notebook shows the configuration options and how to use the chip.fail glitcher.
# We start by configuring the path to the serial device of the FPGA. Note that the Cmod A7 shows up as two serial ports, you can figure out which one is the right one by trial and error.


SERIAL_DEVICE = "/dev/ttyUSB0"

# Next we set up the different parameters for the glitch:

#### POWER_CYCLE_BEFORE_GLITCH
# Whether the DUT should be power-cycled before the test. Some devices are very slow to start up (for example the ESP32), and as such it makes more sense to try to glitch and endless loop.

#### POWER_CYCLE_PULSE
# The duration for which the power-cycle pulse should be send, in 100_000_000th of a second

#### DELAY_FROM - DELAY_TO
# The delay range from the trigger to the glitch that should be tested, in 100_000_000th of a second

#### PULSE_FROM - PULSE_TO
# The duration range for the glitch pulse, in 100_000_000th of a second.

POWER_CYCLE_BEFORE_GLITCH = False
POWER_CYCLE_PULSE = 3_000
DELAY_FROM = 100_000
DELAY_TO = 150_000
PULSE_FROM = 1
PULSE_TO = 100

# Next, we import our basic requirements.

import serial
import struct
from tqdm import trange, tqdm
import time

# In this part we define the commands that are implemented on the FPGA and open the serial device.
# We also establish some helper functions for interacting with the FPGA.

device = serial.Serial(SERIAL_DEVICE, baudrate=115200)
CMD_TOGGLE_LED = 65
CMD_POWER_CYCLE = 66
CMD_SET_GLITCH_PULSE = 67 # uint32
CMD_SET_DELAY = 68 # uint32
CMD_SET_POWER_PULSE = 69 # uint32
CMD_GLITCH = 70
CMD_READ_GPIO = 71
CMD_ENABLE_GLITCH_POWER_CYCLE = 72 # bool/byte
CMD_GET_STATE = 73 # Get state of device

def cmd_toggle_led(device):
    device.write(chr(CMD_TOGGLE_LED).encode("ASCII"))

def cmd(device, command):
    device.write(chr(command).encode("ASCII"))

def cmd_uint32(device, command, u32):
    device.write(chr(command).encode("ASCII"))
    data = struct.pack(">L", u32)
    device.write(data)

def cmd_uint8(device, command, u8):
    device.write(chr(command).encode("ASCII"))
    data = struct.pack("B", u8)
    device.write(data)

def cmd_read_uint8(device, command):
    device.write(chr(command).encode("ASCII"))
    return device.read(1)[0]

def parse_status(status):
    power_pulse_status = (status >> 6) & 0b11
    trigger_status = (status >> 4) & 0b11
    delay_status = (status >> 2) & 0b11
    glitch_pulse_status = status & 0b11
    print("  Power pulse   : " + str(power_pulse_status))
    print("  Trigger status: " + str(trigger_status))
    print("  Delay status  : " + str(delay_status))
    print("  Glitch pulse  : " + str(glitch_pulse_status))

# Lets see what the current state of the glitching logic is.
# This is useful to verify that the device is working and to ensure it does not need to be reset:

status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)

# Here is a simple demo setup of a glitch, with the power pulse, the delay,
# and the glitch pulse set to 1 second each. If this is run, LED1 should light
# up for a second, then a trigger (from low to high) is expected on pin 46,
# then a delay of 1 second is executed and then finally a 1 second glitch-pulse
# will be put out on port 48/LED2.

cmd_uint32(device, CMD_SET_POWER_PULSE, 100_000_000)
cmd_uint32(device, CMD_SET_DELAY, 100_000_000)
cmd_uint32(device, CMD_SET_GLITCH_PULSE, 100_000_000)
cmd_uint8(device, CMD_ENABLE_GLITCH_POWER_CYCLE, 1)

cmd(device, CMD_GLITCH)
print("Step one, power pulse:")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
time.sleep(1.1)

print("Step two, trigger")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
print("\nWaiting for pin to go low...")
while(status == 0b00010000):
    status = cmd_read_uint8(device, CMD_GET_STATE)
print("Got it!")

print("\nWaiting for pin to go high...")
while(status == 0b00100000):
    status = cmd_read_uint8(device, CMD_GET_STATE)
print("Got it!")

print("Step three, delay:")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
time.sleep(1.1)
print("Step four, glitch pulse:")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
while(status == 0b00000001):
    status = cmd_read_uint8(device, CMD_GET_STATE)
print("\nDone, if you get here it means everything is working!")

success = False
for delay in trange(DELAY_FROM, DELAY_TO):
    cmd_uint32(device, CMD_SET_DELAY, delay)
    if success:
        break
    for pulse in trange(PULSE_FROM, PULSE_TO, leave=False):
        cmd_uint32(device, CMD_SET_GLITCH_PULSE, pulse)
        cmd(device, CMD_GLITCH)
        # Loop until the status is == 0, aka the glitch is done.
        # This avoids having to manually time the glitch :)
        while(cmd_read_uint8(device, CMD_GET_STATE)):
            pass
        # Check whether the glitch was successful!
        gpios = cmd_read_uint8(device, CMD_READ_GPIO)
        if gpios:
            print("*** SUCCESS ***")
            print("Delay: " + str(delay))
            print("Pulse: " + str(pulse))
            success = True
            break

# Show status of IOs
print(format(cmd_read_uint8(device, CMD_READ_GPIO), '#010b'))

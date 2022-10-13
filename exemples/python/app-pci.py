#!/usr/bin/python3

import os, sys
from fcntl import ioctl
import time

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

def main():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)

    # data to write
    data = 0x40404079;
    ioctl(fd, WR_R_DISPLAY)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print("wrote %d bytes"%retval)

    # data to write
    data = 0x79404040;
    ioctl(fd, WR_L_DISPLAY)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print("wrote %d bytes"%retval)

    data = 0b000000000000000001
    data1 = 0b10000000

    while(True):

        # data to write
        ioctl(fd, WR_RED_LEDS)
        retval = os.write(fd, int(data).to_bytes(4, 'little'))
        # print("wrote %d bytes"%retval)

        ioctl(fd, WR_GREEN_LEDS)
        retval = os.write(fd, int(data1).to_bytes(4, 'little'))

        ioctl(fd, RD_PBUTTONS)
        red = os.read(fd, 4); # read 4 bytes and store in red var
        print("but 0x%X"%int.from_bytes(red, 'little'))

        ioctl(fd, RD_SWITCHES)
        red1 = os.read(fd, 4); # read 4 bytes and store in red var
        print("sw 0x%X"%int.from_bytes(red1, 'little'))

        data <<=1
        data1 >>=1

        if(data > 0b100000000000000000):
            data = 0b000000000000000001

        if(data1 == 0):
            data1 = 0b10000000

        time.sleep(int.from_bytes(red1, 'little')/int(0b111111111111111111))

    os.close(fd)

if __name__ == '__main__':
    main()


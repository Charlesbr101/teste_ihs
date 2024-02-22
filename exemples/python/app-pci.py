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

# RD_SWITCHES   = ord('a') << (4*2) | ord('a')
# RD_PBUTTONS   = ord('a') << (4*2) | ord('b')
# WR_L_DISPLAY  = ord('a') << (4*2) | ord('c')
# WR_R_DISPLAY  = ord('a') << (4*2) | ord('d')
# WR_RED_LEDS   = ord('a') << (4*2) | ord('e')
# WR_GREEN_LEDS = ord('a') << (4*2) | ord('f')

Vec_7 = [0b01000000, 0b01111001, 0b00100100, 0b00110000, 0b00011001, 0b00010010, 0b00000010, 0b11111000, 0b00000000, 0b00010000]

def main():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)

    data = 0b000000000000000001
    data1 = 0b10000000
    data3 = 0b0
    
    cnt = 0

    while(True):

        # data to write
        ioctl(fd, WR_RED_LEDS)
        retval = os.write(fd, int(data).to_bytes(4, 'little'))
        print("wrote %d bytes in rleds"%retval)

        ioctl(fd, WR_GREEN_LEDS)
        retval = os.write(fd, int(data1).to_bytes(4, 'little'))
        print("wrote %d bytes in gleds"%retval)

        ioctl(fd, RD_PBUTTONS)
        red = os.read(fd, 4); # read 4 bytes and store in red var
        print("but "+ bin(int.from_bytes(red, 'little')))
	
        ioctl(fd, RD_SWITCHES)
        red1 = os.read(fd, 4); # read 4 bytes and store in red var
        print("sw " + bin(int.from_bytes(red1, 'little')))

        data3 = Vec_7[int(cnt%10)] + \
        		(Vec_7[int((cnt/10)%10)] << 8) + \
        		(Vec_7[int((cnt/100)%10)] << 16) + \
        		(Vec_7[int((cnt/1000)%10)] << 24)
        
        ioctl(fd, WR_R_DISPLAY)
        retval = os.write(fd, data3.to_bytes(4, 'little'))
        print("wrote %d bytes in rdisp"%retval)

        data3 = Vec_7[int((cnt/10000)%10)] \
        		+ (Vec_7[int((cnt/100000)%10)] << 8) \
        		+ (Vec_7[int((cnt/1000000)%10)] << 16) \
        		+ (Vec_7[int((cnt/10000000)%10)] << 24)
        
        ioctl(fd, WR_L_DISPLAY)
        retval = os.write(fd, data3.to_bytes(4, 'little'))
        print("wrote %d bytes in ldisp"%retval)

        data <<=1
        data1 >>=1
        cnt+=1

        if(data > 0b100000000000000000):
            data = 0b000000000000000001

        if(data1 == 0):
            data1 = 0b10000000
            
        if(cnt > 99999999):
        	cnt = 0

        time.sleep(int.from_bytes(red1, 'little')/int(0b111111111111111111))

    os.close(fd)

if __name__ == '__main__':
    main()


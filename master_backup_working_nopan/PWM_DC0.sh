#!/bin/bash
#Prereq: Run init script to turn on PWM0 and Global PWM
#
#Set frequency registers (0x18 and 0x17) to 0x0000
spi_xfer -b 1 -c 1 -d 0098 -w 2
spi_xfer -b 1 -c 1 -d 0097 -w 2
#
#Set duty registers (0x32 and 0x31) to 0x0000
spi_xfer -b 1 -c 1 -d 00B2 -w 2
spi_xfer -b 1 -c 1 -d 00B1 -w 2

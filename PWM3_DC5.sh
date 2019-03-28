#!/bin/bash
#Prereq: Run init script to turn on PWM0 and Global PWM
#
#Set frequency registers (0x1E and 0x1D) to 0x30D4
spi_xfer -b 1 -c 1 -d 309E -w 2
spi_xfer -b 1 -c 1 -d D49D -w 2
#
#Set duty registers (0x38 and 0x37) to 0x04FB
spi_xfer -b 1 -c 1 -d 04B8 -w 2
spi_xfer -b 1 -c 1 -d FBB7 -w 2

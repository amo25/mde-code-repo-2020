#!/bin/bash
#Prereq: Run init script to turn on PWM0 and Global PWM
#
#Set frequency registers (0x20 and 0x1F) to 0x30D4
spi_xfer -b 1 -c 1 -d 30A0 -w 2
spi_xfer -b 1 -c 1 -d D49F -w 2
#
#Set duty registers (0x3A and 0x39) to 0x04FB
spi_xfer -b 1 -c 1 -d 04BA -w 2
spi_xfer -b 1 -c 1 -d FBB9 -w 2

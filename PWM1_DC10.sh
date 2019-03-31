#!/bin/bash
#Prereq: Run init script to turn on PWM0 and Global PWM
#
#Set frequency registers (0x1A and 0x19) to 0x30D4
spi_xfer -b 1 -c 1 -d 309A -w 2
spi_xfer -b 1 -c 1 -d D499 -w 2
#
#Set duty registers (0x34 and 0x33) to 0x09F6
spi_xfer -b 1 -c 1 -d 09B4 -w 2
spi_xfer -b 1 -c 1 -d F6B3 -w 2

#!/bin/bash
#Prereq: Run init script to turn on PWM0 and Global PWM
#
#Set frequency registers (0x18 and 0x17) to 0x30D4
spi_xfer -b 1 -c 1 -d 3098 -w 2
spi_xfer -b 1 -c 1 -d D497 -w 2
#
#Set duty registers (0x32 and 0x31) to 0x3BC4
spi_xfer -b 1 -c 1 -d 3BB2 -w 2
spi_xfer -b 1 -c 1 -d C4B1 -w 2

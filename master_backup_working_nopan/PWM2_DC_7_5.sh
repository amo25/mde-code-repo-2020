#!/bin/bash
#Get 7.5% Duty Cycle at 50Hz (light center)
#Prereq: Run init script to turn on PWM0 and Global PWM
#
#Set frequency registers (0x1C and 0x1B) to 0x30D4
spi_xfer -b 1 -c 1 -d 309C -w 2
spi_xfer -b 1 -c 1 -d D49B -w 2
#
#Set duty registers (0x36 and 0x35) to 0x0778
spi_xfer -b 1 -c 1 -d 07B6 -w 2
spi_xfer -b 1 -c 1 -d 78B5 -w 2

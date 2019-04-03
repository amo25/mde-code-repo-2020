#!/bin/bash
#Initialize PWM0
#Set PWM Global Enable
spi_xfer -b 1 -c 1 -d 8096 -w 2
#
#Set PWM0-7 Enable
spi_xfer -b 1 -c 1 -d FF95 -w 2

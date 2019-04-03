#!/bin/bash
#Initialize PWM0
#Disable PWM Global Enable
spi_xfer -b 1 -c 1 -d 0096 -w 2
#
#Disable all PWMs
spi_xfer -b 1 -c 1 -d 0095 -w 2

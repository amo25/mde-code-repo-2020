#!/bin/bash
#Initialize PWM0
#Set PWM Global Enable
spi_xfer -b 1 -c 1 -d 8096 -w 2
#
#Set PWM0, PWM1, and PWM2 Enable
spi_xfer -b 1 -c 1 -d 0795 -w 2

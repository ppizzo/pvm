#!/bin/sh
#
# Photovoltaic Monitor
#
# Photovoltaic production monitoring using RS485 interface
# to Kaco inverters.
#
# This script starts the main program.
#
# 2012, Pietro Pizzo <pietro.pizzo@gmail.com>
######################################################################

cd `dirname $0`
nohup ./pvm.py &

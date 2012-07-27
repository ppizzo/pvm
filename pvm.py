#!/usr/bin/python
#
# Photovoltaic Monitor
#
# Photovoltaic production monitoring using RS485 interface
# to Kaco inverters.
#
# 2012, Pietro Pizzo <pietro.pizzo@gmail.com>
######################################################################

import logging
import mylib

logging.info("PVM started")

import time
import db
import rs485

# Start RS485 threads
rs485.start_read()
rs485.start_write()

time.sleep(60000)
rs485.stop_all()

logging.info("PVM stopping")

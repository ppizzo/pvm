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
import time
import db
logging.info("PVM started")

import db
import rs485

# Start write/read to/from inverter
#rs485.start_read()
#rs485.start_details_write()
#rs485.start_totals_write()
rs485.start_read_write()

time.sleep(60000)
rs485.stop_all()

logging.info("PVM stopping")

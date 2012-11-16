#!/usr/bin/python3
#
# PVM PhotoVoltaic Monitor.
# Photovoltaic production monitoring using RS485 interface
# to Kaco inverters.
#
# Depends: python3-serial
#
# Copyright (C) 2012 Pietro Pizzo <pietro.pizzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

import logging
import mylib

logging.info("PVM started")

import time
import db
import rs485

# Start RS485 threads
rs485.start_all()

#rs485.stop_all()

#logging.info("PVM stopping")

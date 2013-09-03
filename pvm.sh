#!/bin/sh
#
# PVM PhotoVoltaic Monitor
# Photovoltaic production monitoring using RS485 interface
# to Kaco inverters.
#
# This script starts the main program.
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

cd `dirname $0`

# Read configuration file
eval $(cat config |grep rs485_usb_id)

# Test RS485 presence
lsusb -d ${rs485_usb_id} >/dev/null 2>&1
if [ "$?" -ne "0" ]; then
    echo "RS485 not found. Exiting." >&2
    exit 1
fi

nohup ./pvm.py &

#
# PVM PhotoVoltaic Monitor.
# Real time production statistic module
#
# Copyright (C) 2013 Pietro Pizzo <pietro.pizzo@gmail.com>
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

import mylib
import db
import logging

def write(d):
    """Write real time statistics on file."""
    try:
        fd = open(mylib.config_rtfile, "w")
    except Exception as e:
        logging.error(e, "Cannot open \""+mylib.config_rtfile+"\" for writing. Real time stats will not be available")
        return

    print("timestamp=", d.timestamp, "&", sep="", end="", file=fd)
    print("status=", d.status, "&", sep="", end="", file=fd)
    print("generator_voltage=", d.generator_voltage, "&", sep="", end="", file=fd)
    print("generator_current=", d.generator_current, "&", sep="", end="", file=fd)
    print("generator_power=", d.generator_power, "&", sep="", end="", file=fd)
    print("grid_voltage=", d.grid_voltage, "&", sep="", end="", file=fd)
    print("grid_current=", d.grid_current, "&", sep="", end="", file=fd)
    print("delivered_power=", d.delivered_power, "&", sep="", end="", file=fd)
    print("device_temperature=", d.device_temperature, "&", sep="", end="", file=fd)
    print("daily_yeld=", d.daily_yeld, sep="", file=fd)

    fd.close()

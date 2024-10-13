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

import json
import mylib
import db
import logging

"""Write stats on text file"""
def write(d):
    # Write text file
    try:
        with open(mylib.config_rtfile, "w") as file:
            for k, v in vars(d).items():
                print(k, v, sep="=", end="&", file=file)
    except Exception as e:
        logging.error(f"Error: {e}. Real time stats will not be available")
        return

    # Write JSON file
    try:
        with open(mylib.config_rtfile_json, "w") as file:
            json.dump(vars(d), file)
    except Exception as e:
        logging.error(f"Error: {e}. Real time stats will not be available")
        return

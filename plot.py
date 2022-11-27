#!/usr/bin/python3
#
# PVM PhotoVoltaic Monitor.
# Data plot module
#
# Copyright (C) 2012,2013 Pietro Pizzo <pietro.pizzo@gmail.com>
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
import sys
import subprocess
import logging

def write_result(file, result):
    """Write result to file suitable for gnuplot"""
    for row in result:
            for field in row[:-1]:
                print(field, end="", file=file)
                print("\t", end="", file=file)
            print(row[-1:][0], file=file)

def plot_daily_details(date):
    """Daily details plot"""

    try:
        file = open(mylib.config_output_dir + "/" + mylib.config_daily_details_plot_file, mode="w")

        result = db.read_daily_details(date)
        write_result(file, result)

        file.close()
    except Exception as e:
        logging.error(e)

def plot_monthly_stats(date):
    """Monthly stats plot"""

    try:
        file = open(mylib.config_output_dir + "/" + mylib.config_monthly_stats_plot_file, mode="w")

        result = db.read_monthly_stats(date)
        write_result(file, result)

        file.close()
    except Exception as e:
        logging.error(e)

def plot_yearly_stats(date):
    """Yearly stats plot"""

    try:
        file = open(mylib.config_output_dir + "/" + mylib.config_yearly_stats_plot_file, mode="w")

        result = db.read_yearly_stats(date)
        write_result(file, result)

        file.close()
    except Exception as e:
        logging.error(e)

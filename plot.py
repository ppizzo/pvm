#!/usr/bin/python3
#
# Photovoltaic Monitor - Data plot module
#
# 2012, Pietro Pizzo <pietro.pizzo@gmail.com>
######################################################################

import mylib
import db
import sys
import subprocess

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

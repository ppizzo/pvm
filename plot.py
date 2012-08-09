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

def plot_daily_details(date):
    """Daily details plot"""

    try:
        file = open(mylib.config_output_dir + "/" + mylib.config_plot_file, mode="w")

        result = db.read_daily_details(date)
        for row in result:
            for field in row[:-1]:
                print(field, end="", file=file)
                print("\t", end="", file=file)
            print(row[-1:][0], file=file)

    except Exception as e:
        logging.error(e)

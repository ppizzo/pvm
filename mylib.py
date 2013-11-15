#
# PVM PhotoVoltaic Monitor.
# Library module
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

import logging
import datetime
import configparser

# Config filename
CONFIG_FILE = "config"

# Confguration file parsing
c = configparser.ConfigParser()
c.read(CONFIG_FILE)

config_dbfile = c.get("main", "dbfile")
config_rtfile = c.get("main", "rtfile")
config_logfile = c.get("main", "logfile")
config_loglevel = c.get("main", "loglevel")
config_serialdev = c.get("main", "serialdev")
config_details_delay = float(c.get("main", "details_delay"))
config_totals_delay = float(c.get("main", "totals_delay"))
config_monitor_start_time=c.get("main", "monitor_start_time")
config_monitor_stop_time=c.get("main", "monitor_stop_time")
config_housekeeping_start_time=c.get("main", "housekeeping_start_time")
config_output_dir=c.get("main", "output_dir")
config_daily_details_plot_file=c.get("main", "daily_details_plot_file")
config_monthly_stats_plot_file=c.get("main", "monthly_stats_plot_file")
config_yearly_stats_plot_file=c.get("main", "yearly_stats_plot_file")

if config_loglevel == "debug":
    loglevel = logging.DEBUG
elif config_loglevel == "info":
    loglevel = logging.INFO
elif config_loglevel == "warning":
    loglevel = logging.WARNING
elif config_loglevel == "ERROR":
    loglevel = logging.ERROR
elif config_loglevel == "critical":
    loglevel = logging.CRITICAL
else:
    loglevel = logging.INFO

# Logging configuration
logging.basicConfig(filename=config_logfile, format='%(asctime)s [%(levelname)s] %(message)s', level=loglevel)

def datetimestamp():
    """Returns the current timestamp in a format suitable for DB import"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def timestamp():
    """Returns the current time"""
    return datetime.datetime.now().strftime("%H:%M:%S")

def datestamp():
    """Returns the current date (without time)"""
    return datetime.datetime.now().strftime("%Y-%m-%d")

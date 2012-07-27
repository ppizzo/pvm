import logging
import datetime
import configparser

# Config filename
CONFIG_FILE = "config"

# Confguration file parsing
c = configparser.ConfigParser()
c.read(CONFIG_FILE)

config_dbfile = c.get("main", "dbfile")
config_logfile = c.get("main", "logfile")
config_loglevel = c.get("main", "loglevel")
config_serialdev = c.get("main", "serialdev")
config_details_delay = float(c.get("main", "details_delay"))
config_totals_delay = float(c.get("main", "totals_delay"))
config_monitor_start_time=c.get("main", "monitor_start_time")
config_monitor_stop_time=c.get("main", "monitor_stop_time")
config_housekeeping_start_time=c.get("main", "housekeeping_start_time")

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

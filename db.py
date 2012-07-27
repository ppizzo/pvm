import mylib
import sqlite3
import logging
import sys

try:
    # DB initialization and check
    conn = sqlite3.connect(mylib.config_dbfile)
    cur = conn.cursor()
    cur.execute("pragma journal_mode=wal")
    if (cur.fetchone()[0] != "wal"):
        logging.warning("Cannot set DB in Write-Ahead Logging (WAL) mode. Expect some queries to fail")
    cur.close()
    conn.close()
    logging.debug("Connected to database")
except Exception as e:
    logging.critical(e)
    logging.info("PVM stopping")
    sys.exit()

class DailyDetails:
    """Class to hold detail snapshot data (01 request)"""
    timestamp = None
    status = None
    generator_voltage = None
    generator_current = None
    generator_power = None
    grid_voltage = None
    grid_current = None
    delivered_power = None
    device_temperature = None
    daily_yeld = None
    checksum = None
    inverter_type = None

class DailyTotals:
    """Class to hold daily total data (03 request)"""
    timestamp = None
    daily_max_delivered_power = None
    daily_delivered_power = None
    total_delivered_power = None
    partial_delivered_power = None
    daily_running_hours = None
    total_running_hours = None
    partial_running_hours = None

def write_daily_details(d):
    """Writes a daily details line on DB"""
    try:
        conn = sqlite3.connect(mylib.config_dbfile)
        cursor = conn.cursor()
        vals = (d.timestamp, d.status, d.generator_voltage, d.generator_current,
                d.generator_power, d.grid_voltage, d.grid_current, d.delivered_power,
                d.device_temperature, d.daily_yeld)

        cursor.execute("""insert into daily_details(timestamp, status, generator_voltage,
            generator_current, generator_power, grid_voltage, grid_current, delivered_power,
            device_temperature, daily_yeld) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", vals)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(e)

def write_daily_totals(d):
    """Writes a daily totals line on DB"""
    try:
        conn = sqlite3.connect(mylib.config_dbfile)
        cursor = conn.cursor()
        vals = (d.timestamp, d.daily_max_delivered_power, d.daily_delivered_power,
                d.total_delivered_power, d.partial_delivered_power, d.daily_running_hours,
                d.total_running_hours, d.partial_running_hours)

        cursor.execute("""insert into daily_totals(timestamp, daily_max_delivered_power,
            daily_delivered_power, total_delivered_power, partial_delivered_power,
            daily_running_hours, total_running_hours, partial_running_hours)
            values (?, ?, ?, ?, ?, ?, ?, ?)""", vals)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(e)


# Query functions
def read_daily_details(date):
    """Retrieves daily stats"""
    try:
        conn = sqlite3.connect(mylib.config_dbfile)
        cursor = conn.cursor()

        cursor.execute("""select rowid, time(timestamp) as time, status,
            generator_voltage, generator_current, generator_power,
            grid_voltage, grid_current, delivered_power,
            device_temperature, daily_yeld from daily_details
            where date(timestamp) = ?""", (date,))

        result = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        return result
    except Exception as e:
        logging.error(e)

# Housekeeping functions
def clean_daily_totals():
    """Deletes all rows but last one on current day on daily_totals"""
    try:
        conn = sqlite3.connect(mylib.config_dbfile)
        cursor = conn.cursor()

        cursor.execute("delete from daily_totals where rowid < (select max(rowid) from daily_totals where date(timestamp)=date()) and date(timestamp)=date()")

        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Housekeeping: cleaned up daily totals")
    except Exception as e:
        logging.error(e)


import serial
import threading
import time
import mylib
import db
import sys
import logging

# Handmade sem: True means "continue thread", False means "stop"
go = True

# Inverter commands
DAILY_DETAILS_CMD = "#010\r"
DAILY_TOTALS_CMD = "#013\r"

# Serial port definition
try:
    ser = serial.Serial(
        port=mylib.config_serialdev,
        baudrate=9600,
        timeout=None,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
except Exception as e:
    logging.critical(e)
    logging.info("PVM stopping")
    # FIXME: print statement to be removed after development
    print e
    sys.exit()

class AsyncWriteRS485(threading.Thread):
    """Async inverter interface write class"""
    def __init__(self, ser, details_delay, totals_delay):
        threading.Thread.__init__(self)
        self.ser = ser
        self.details_delay = details_delay
        self.totals_delay = totals_delay
        self.totals_freq = int(self.totals_delay / self.details_delay)
    def run(self):
        logging.info("RS485 write thread started")
        count = 0
        global go
        while go:

            # Write request
            self.ser.write(DAILY_DETAILS_CMD)

            # Every 'totals_freq' details request total stats
            if (count % self.totals_freq == 0):
                count = 0
                time.sleep(self.details_delay / 2 - 1)
                self.ser.write(DAILY_TOTALS_CMD)
                time.sleep(self.details_delay / 2)
            else:
                time.sleep(self.details_delay)

            count = count + 1

        logging.info("RS485 write thread stopped")

class AsyncReadRS485(threading.Thread):
    """Async inverter interface read class"""
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.initial_chars = 5
        self.details_remaining_chars = 66 - self.initial_chars
        self.total_remaining_chars = 63 - self.initial_chars
    def run(self):
        logging.info("RS485 read thread started")
        count = 0
        global go
        while go:

            # Read header
            header = self.ser.read(self.initial_chars)[1:]

            data = ""
            timestamp = mylib.timestamp()

            # Reads response command type and decide what to do
            command = header[3:4]
            if (command == "0"):
                # Read remaining chars
                data = self.ser.read(self.details_remaining_chars)[:-1]

                daily_details = db.DailyDetails()
                daily_details.timestamp = timestamp
                daily_details.status = data[3:4]
                daily_details.generator_voltage = data[5:10]
                daily_details.generator_current = data[11:16]
                daily_details.generator_power = data[17:22]
                daily_details.grid_voltage = data[23:28]
                daily_details.grid_current = data[29:34]
                daily_details.delivered_power = data[35:40]
                daily_details.device_temperature = data[41:44]
                daily_details.daily_yeld = data[45:51]
                daily_details.checksum = data[52:53]
                daily_details.inverter_type = data[54:60]

                db.write_daily_details(daily_details)

            elif (command == "3"):
                # Read remaining chars
                data = self.ser.read(self.total_remaining_chars)[:-1]

                daily_totals = db.DailyTotals()
                daily_totals.timestamp = timestamp
                daily_totals.daily_max_delivered_power = data[1:6]
                daily_totals.daily_delivered_power = data[7:13]
                daily_totals.total_delivered_power = float(data[14:20]) / 10
                daily_totals.partial_delivered_power = float(data[21:27]) / 10
                daily_totals.daily_running_hours = data[28:37].strip()
                daily_totals.total_running_hours = data[38:47].strip()
                daily_totals.partial_running_hours = data[48:57].strip()

                db.write_daily_totals(daily_totals)

            else:
                logging.warning("RS485 invalid command response: " + command)
                # TODO: go ahead until a "*01" string appears and resync the input stream

            logging.debug("Inverter: " + header + data)

        logging.info("RS485 read thread stopped")

# Initialization
fd = ser.fileno()

def start_write():
    global write_task
    write_task = AsyncWriteRS485(ser, mylib.config_details_delay, mylib.config_totals_delay)
    write_task.start()

def start_read():
    global read_task
    read_task = AsyncReadRS485(ser)
    read_task.start()

def stop_all():
    logging.info("Waiting for RS485 threads to stop")
    global go
    global write_task
    global read_task
    go = False;
    write_task.join()
    read_task.join()
    logging.info("All RS485 threads stopped")

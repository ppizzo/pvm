import serial
#import fcntl
#import struct
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
    # FIXME
    print e
    sys.exit()

class AsyncReadWriteRS485(threading.Thread):
    """Async daily details read thread"""
    def __init__(self, ser, details_delay, totals_delay):
        threading.Thread.__init__(self)
        self.ser = ser
        self.details_delay = details_delay
        self.totals_delay = totals_delay
        self.totals_freq = int(self.totals_delay / self.details_delay)
        self.initial_chars = 5
        self.details_remaining_chars = 66 - self.initial_chars
        self.total_remaining_chars = 63 - self.initial_chars
    def run(self):
        logging.info("RS485 read/write thread started")
        count = 0
        global go
        while go:

            # Write request
            if (count % self.totals_freq != 0):
                self.ser.write(DAILY_DETAILS_CMD)
            else:
                self.ser.write(DAILY_TOTALS_CMD)

            # Read answer
            header = self.ser.read(self.initial_chars)[1:]
            #header = "*010"
            data = ""
            timestamp = mylib.timestamp()

            # Reads response command type and decide what to do
            command = header[3:4]
            if (command == "0"):
                data = self.ser.read(self.details_remaining_chars)[:-1]
                #data = "   4 389.7 10.48  4085 236.5 16.58  3922  46  20704 X SP4600"
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
                #data = "  4117  20705   3848   3848      8:15    186:52    186:52"
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
            count = count + 1

            # Every 10 details, reads 1 total (in this case no delay)
            if (count % self.totals_freq != 0):
                time.sleep(self.delay)

        logging.info("RS485 read/write thread stopped")

# Initialization
fd = ser.fileno()

def start_read_write():
    global read_write_task
    read_write_task = AsyncReadWriteRS485(ser, mylib.config_details_delay, mylib.config_totals_delay)
    read_write_task.start()

def stop_all():
    logging.info("Waiting for RS485 threads to stop")
    global go
    global read_write_task
    go = False;
    read_write_task.join()
    logging.info("All RS485 threads stopped")

import serial
import threading
import time
import mylib
import db
import sys
import logging

# Handmade sem: True means "continue thread", False means "stop"
go = True

# Inverter type
INVERTER_TYPE = "SP4600"

# Inverter commands
DAILY_DETAILS_CMD = "#010\r"
DAILY_TOTALS_CMD = "#013\r"

# Inverter responses
DAILY_DETAILS_RES = "\n*010"
DAILY_TOTALS_RES = "\n*013"

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
    print(e)
    sys.exit()

# Initialization
fd = ser.fileno()

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
            self.ser.write(bytes(DAILY_DETAILS_CMD, "ascii"))

            # Every 'totals_freq' details request total stats
            if (count % self.totals_freq == 0):
                count = 0
                time.sleep(self.details_delay / 2 - 1)
                self.ser.write(bytes(DAILY_TOTALS_CMD, "ascii"))
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
        self.header_chars = len(DAILY_DETAILS_RES)
        self.details_remaining_chars = 66 - self.header_chars
        self.total_remaining_chars = 63 - self.header_chars
    def run(self):
        logging.info("RS485 read thread started")
        global go
        while go:

            # Go ahead until a "\n*" string appears to identify the starting of header
            skip_prev = self.ser.read(1).decode(encoding="ascii", errors="replace")
            skip = self.ser.read(1).decode(encoding="ascii", errors="replace")
            while (skip_prev + skip != "\n*"):
                skip_prev = skip
                skip = self.ser.read(1).decode(encoding="ascii", errors="replace")

            # Read remaining part of header
            header = skip_prev + skip + self.ser.read(self.header_chars - 2).decode(encoding="ascii", errors="replace")
            if (len(header) != self.header_chars):
                logging.warning("Unexpected header length: read " + str(len(header)) + " chars, expected " + str(self.header_chars))
                continue

            data = ""
            timestamp = mylib.datetimestamp()

            # Reads response command type and decide what to do
            if (header == DAILY_DETAILS_RES):
                # Read remaining chars
                data = self.ser.read(self.details_remaining_chars).decode(encoding="ascii", errors="replace")
                if (len(data) != self.details_remaining_chars):
                    logging.warning("Unexpected data length: read " + str(len(data)) + " chars, expected " + str(self.details_remaining_chars))
                    continue

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

                # Formal checks
                if (daily_details.inverter_type != INVERTER_TYPE):
                    logging.warning("Inverter type does not match: found '" +
                                    daily_details.inverter_type + "', expected '" +
                                    INVERTER_TYPE + "'")
                    continue
                #if (daily_details.checksum != checksum(header[1:] + data[:-9])):
                #    logging.warning("Wrong checksum")
                #    continue

                db.write_daily_details(daily_details)
                logging.debug("Inverter: '" + header[1:] + data[:-1] + "'")

            elif (header == DAILY_TOTALS_RES):
                # Read remaining chars
                data = self.ser.read(self.total_remaining_chars).decode(encoding="ascii", errors="replace")
                if (len(data) != self.total_remaining_chars):
                    continue

                daily_totals = db.DailyTotals()
                daily_totals.timestamp = timestamp
                daily_totals.daily_max_delivered_power = data[1:6]
                daily_totals.daily_delivered_power = data[7:13]
                try:
                    daily_totals.total_delivered_power = float(data[14:20]) / 10
                    daily_totals.partial_delivered_power = float(data[21:27]) / 10
                except Exception as e:
                    logging.warning(e)
                    continue
                daily_totals.daily_running_hours = data[28:37].strip()
                daily_totals.total_running_hours = data[38:47].strip()
                daily_totals.partial_running_hours = data[48:57].strip()

                db.write_daily_totals(daily_totals)
                logging.debug("Inverter: '" + header[1:] + data[:-1] + "'")

            else:
                logging.warning("RS485 unhandled or invalid command response: '" + header[1:] + "'")

        logging.info("RS485 read thread stopped")

def checksum(s):
    """Calculate the checksum of the input string"""
    c = 0
    for i in s:
        c = c + ord(i)
    return chr(c & 0xff)

def start_write():
    global write_task
    write_task = AsyncWriteRS485(ser, mylib.config_details_delay, mylib.config_totals_delay)
    write_task.start()

def start_read():
    global read_task
    read_task = AsyncReadRS485(ser)
    read_task.start()

def start_all():
    start_read()
    start_write()

def stop_all():
    logging.info("Waiting for RS485 threads to stop")
    global go
    global write_task
    global read_task
    go = False;
    write_task.join()
    read_task.join()
    logging.info("All RS485 threads stopped")

from taipy.gui import Gui, State, invoke_callback, get_state_id
import taipy.gui.builder as tgb
from threading import Thread
import time, random
from datetime import datetime, timedelta
import db #, mylib

# Gui refresh delay
delay = 5 #mylib.config_details_delay

# Global variables holding data to be shown on the gui
realtime, daily_stats, monthly_stats, yearly_stats = {}, {}, {}, {}
date = datetime.today().date()

# Gui state ID (single user mode)
state_id = None

def create_page():
    # Page layout
    with tgb.Page() as page:
        tgb.text("# PVM &mdash; PhotoVoltaic Monitor", mode="md")

        with tgb.layout("1 3", gap="20px", class_name="align_column_center"):
            tgb.text("⌚️ _{realtime['timestamp'].item()}_", mode="md")
            with tgb.layout("5 1 1 1 20", class_name="align_columns_center"):
                tgb.date("{date}", format="PP", on_change="change_date")
                tgb.button(label="◀", hover_text="Day - 1", on_action="yesterday")
                tgb.button(label="Today", hover_text="Today", on_action="today")
                tgb.button(label="▶", hover_text="Day + 1", on_action="tomorrow")
                tgb.part()
            with tgb.part():
                tgb.text("#### ☀️ Generator", mode="md")
                with tgb.layout("1 1", class_name="container align_columns_center"):
                    tgb.text("Status")
                    tgb.text("{realtime['status'].item()}")
                    tgb.text("Temperature")
                    tgb.text("{realtime['device_temperature'].item()} ºC")
                    tgb.text("Voltage")
                    tgb.text("{realtime['generator_voltage'].item()} V", format="%.1f")
                    tgb.text("Current")
                    tgb.text("{realtime['generator_current'].item()} A", format="%.2f")
                    tgb.text("Power")
                    tgb.text("{realtime['generator_power'].item()} W")

                tgb.text("#### ⚡️ Grid", mode="md")
                with tgb.layout("1 1", class_name="container align_columns_center"):
                    tgb.text("Voltage")
                    tgb.text("{realtime['grid_voltage'].item()} V", format="%.1f")
                    tgb.text("Current")
                    tgb.text("{realtime['grid_current'].item()} A", format="%.2f")

                tgb.text("#### 🔋 Production", mode="md")
                with tgb.layout("1 1", class_name="container align_columns_center"):
                    tgb.text("Delivered power")
                    tgb.text("{realtime['delivered_power'].item()} W")
                    tgb.text("Daily yeld")
                    tgb.text("{realtime['daily_yeld'].item()} W")

            with tgb.part(width="900px"):
                tgb.chart("{daily_stats}", mode="line", x="Time", y="Power", color="red", height="400px")
                tgb.part(height="20px")
                tgb.chart("{monthly_stats}", type="bar", x="Day", y__1="Daily production", y__2="Reference production", color__1="red", color__2="blue", height="400px")
                tgb.part(height="20px")
                tgb.chart("{yearly_stats}", type="bar", x="Month", y__1="Monthly production", y__2="Reference production", color__1="red", color__2="blue", height="400px")

    return page

# Reader thread: read values and update the gui
class read(Thread):
    def __init__(self, gui):
        Thread.__init__(self)
        self.gui = gui

    def run(self):
        global realtime, daily_stats, monthly_stats, yearly_stats

        while True:
            # Wait until the gui is running. Should wait only at startup
            if hasattr(self.gui, "_server") and state_id:
                invoke_callback(self.gui, state_id, update_values)

            # Interval between gui updates
            time.sleep(delay)

# Get the state id
def on_init(state: State):
    global state_id
    state_id = get_state_id(state)

# Buttons callbacks. The date will be set by change_date
def yesterday(state: State): change_date(state, "yesterday", date)
def today(state: State): change_date(state, "today", date)
def tomorrow(state: State): change_date(state, "tomorrow", date)

# Update the values after a date change
def change_date(state: State, var, val):
    global date

    if var == "date":
        date = val
    elif var == "yesterday":
        date -= timedelta(days=1)
    elif var == "tomorrow":
        date += timedelta(days=1)
    elif var == "today":
        date = datetime.today().date()

    # Trigger gui refresh
    update_values(state)

# Update the values within the state
def update_values(state: State):
    # Read stats from DB
    state.daily_stats = db.pread_daily_details(date)
    state.monthly_stats = db.pread_monthly_stats(date)
    state.yearly_stats = db.pread_yearly_stats(date)
    state.realtime = db.pread_realtime()

    state.date = date

if __name__ == "__main__":
    # Create the gui object (here because needed by the read thread)
    gui = Gui(create_page())

    # Start reader thread
    read(gui).start()

    # Start webui
    gui.run(title="PVM", favicon="favicon.ico", single_client=True, host="0.0.0.0", port=9000)

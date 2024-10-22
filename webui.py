import taipy as tp, taipy.gui.builder as tgb
from threading import Thread
import time, random
from datetime import datetime, timedelta
import db, mylib
import pandas as pd

# Gui refresh delay
delay = mylib.config_details_delay

# Global variables holding data to be shown on the gui
date = datetime.today().date()
realtime = db.pread_realtime()
daily_stats = db.pread_daily_details(date)
monthly_stats = db.pread_monthly_stats(date)
yearly_stats = db.pread_yearly_stats(date)

# Gui state ID (single user mode)
state_id = None

def create_page():
    # Page layout
    with tgb.Page() as page:
        tgb.text("# PVM &mdash; PhotoVoltaic Monitor", mode="md")

        with tgb.layout("2 5", gap="20px", class_name="align-column-center"):
            tgb.text("⌚️ _{realtime['timestamp'].item()}_", mode="md")
            with tgb.layout("5 1 1 1 20", class_name="align-columns-center"):
                tgb.date("{date}", format="PP", on_change="change_date")
                tgb.button(label="◀", hover_text="Day - 1", on_action="yesterday")
                tgb.button(label="⏏︎", hover_text="Today", on_action="today")
                tgb.button(label="▶", hover_text="Day + 1", on_action="tomorrow")
                tgb.part()
            with tgb.part():
                tgb.text("#### ☀️ Generator", mode="md")
                with tgb.layout("1 1", class_name="container align-columns-center"):
                    tgb.text("Power (W)", class_name="h5 color-primary")
                    tgb.text("{realtime['generator_power'].item()}", format="%.0f", class_name="h5 color-primary")
                    tgb.text("Status")
                    tgb.text("{realtime['status'].item()}")
                    tgb.text("Temperature (ºC)")
                    tgb.text("{realtime['device_temperature'].item()}", format="%.0f")
                    tgb.text("Voltage (V)")
                    tgb.text("{realtime['generator_voltage'].item()}", format="%.1f")
                    tgb.text("Current (A)")
                    tgb.text("{realtime['generator_current'].item()}", format="%.2f")

                tgb.text("#### ⚡️ Grid", mode="md")
                with tgb.layout("1 1", class_name="container align-columns-center"):
                    tgb.text("Voltage (V)")
                    tgb.text("{realtime['grid_voltage'].item()}", format="%.1f")
                    tgb.text("Current (A)")
                    tgb.text("{realtime['grid_current'].item()}", format="%.2f")

                tgb.text("#### 🔋 Production", mode="md")
                with tgb.layout("1 1", class_name="container align-columns-center"):
                    tgb.text("Delivered power (W)")
                    tgb.text("{realtime['delivered_power'].item()}", format="%.0f")
                    tgb.text("Daily yeld (W)")
                    tgb.text("{realtime['daily_yeld'].item()}", format="%.0f")

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
                tp.gui.invoke_callback(self.gui, state_id, update_values)

            # Interval between gui updates
            time.sleep(delay)

# Get the state id
def on_init(state):
    global state_id
    state_id = tp.gui.get_state_id(state)

    # Initialize variables with the correct datatype
    state.daily_stats = daily_stats
    state.monthly_stats = monthly_stats
    state.yearly_stats = yearly_stats
    state.realtime = realtime

# Buttons callbacks. The date will be set by change_date
def yesterday(state): change_date(state, "yesterday", date)
def today(state): change_date(state, "today", date)
def tomorrow(state): change_date(state, "tomorrow", date)

# Update the values after a date change
def change_date(state, var, val):
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
def update_values(state):
    # Read stats from DB. Updates graphs only if changed, to avoid unnecessary flickering
    if not (daily_stats := db.pread_daily_details(date)).equals(state.daily_stats): state.daily_stats = daily_stats
    if not (monthly_stats := db.pread_monthly_stats(date)).equals(state.monthly_stats): state.monthly_stats = monthly_stats
    if not (yearly_stats := db.pread_yearly_stats(date)).equals(state.yearly_stats): state.yearly_stats = yearly_stats
    state.realtime = db.pread_realtime()
    state.date = date

if __name__ == "__main__":
    # Create the gui object (here because needed by the read thread)
    gui = tp.Gui(create_page())

    # Start reader thread
    read(gui).start()

    # Start webui
    tp.run(gui, title="PVM", favicon="favicon.png", single_client=True, host="0.0.0.0", port=9000)

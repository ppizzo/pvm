from taipy.gui import Gui, State, invoke_callback, get_state_id
import taipy.gui.builder as tgb
from threading import Thread
import time, random
import db, mylib

# Gui refresh delay
delay = 15

# Global variables holding data to be shown on the gui
realtime, daily_stats, monthly_stats, yearly_stats = {}, {}, {}, {}

# Gui state ID (single user mode)
state_id = None

def create_page():
    # Page layout
    with tgb.Page() as page:
        tgb.text("# PVM &mdash; PhotoVoltaic Monitor", mode="md")
        tgb.text("⌚️ _{realtime['timestamp'].item()}_", mode="md")

        with tgb.layout("1fr 3fr", gap="20px", class_name="align_columns_center"):
            with tgb.part():
                tgb.text("#### ☀️ Generator", mode="md")
                with tgb.layout("1fr 1fr", class_name="container align_columns_center"):
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
                with tgb.layout("1fr 1fr", class_name="container align_columns_center"):
                    tgb.text("Voltage")
                    tgb.text("{realtime['grid_voltage'].item()} V", format="%.1f")
                    tgb.text("Current")
                    tgb.text("{realtime['grid_current'].item()} A", format="%.2f")

                tgb.text("#### 🔋 Production", mode="md")
                with tgb.layout("1fr 1fr", class_name="container align_columns_center"):
                    tgb.text("Daily delivered")
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
            daily_stats=db.pread_daily_details(mylib.datestamp())
            monthly_stats=db.pread_monthly_stats(mylib.datestamp())
            yearly_stats=db.pread_yearly_stats(mylib.datestamp())
            realtime=db.pread_realtime()

            if hasattr(self.gui, "_server") and state_id:
                invoke_callback(self.gui, state_id, update_value) #, (value,))
            time.sleep(delay)

# Get the state id
def on_init(state: State):
    global state_id
    state_id = get_state_id(state)

# Update the value within the state
def update_value(state: State):
    state.daily_stats = daily_stats
    state.monthly_stats = monthly_stats
    state.realtime = realtime

if __name__ == "__main__":
    # Create the gui object (here because needed by the read thread)
    gui = Gui(create_page())

    # Start reader thread
    read(gui).start()

    # Start webui
    gui.run(title="PVM", favicon="favicon.ico", single_client=True, host="0.0.0.0", port=9000)

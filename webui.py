from taipy.gui import Gui, State, invoke_callback, get_state_id
import taipy.gui.builder as tgb
from threading import Thread
import time, random
import db, mylib

# Gui refresh delay
delay = 15

# Global variables holding data to be shown on the gui
realtime = {
    "generator": {
        "voltage": 220.1234,
        "current": 1.2345,
        "power": 1.23543
    },
    "grid": {
        "voltage": 0,
        "current": 0
    },
    "production": {
        "power": 0,
        "yeld": 0
    }
}
#daily_stats = {
#    "Time": [],
#    "Power": []
#}
#monthly_stats = {
#    "Time": [],
#    "Production": [],
#    "Reference production": []
#}
#yearly_stats = {
#    "Time": [],
#    "Production": [],
#    "Reference production": []
#}

daily_stats, monthly_stats, yearly_stats = {}, {}, {}

# Gui state ID (single user mode)
state_id = None

def create_page():
    # Page layout
    with tgb.Page() as page:
        tgb.text("# PVM &dash; PhotoVoltaic Monitor", mode="md")
        tgb.text("## Real time monitoring", mode="md")

        with tgb.layout("1fr 3fr", gap="20px", class_name="align_columns_center"):
            with tgb.part():

                tgb.text("#### ☀️ Generator", mode="md")
                with tgb.layout("1fr 3fr", gap="20px", class_name="container align_columns_center"):
                    tgb.part()
                    with tgb.part():
                        tgb.text("Voltage: {realtime['generator']['voltage']} V", format="%.1f")
                        tgb.text("Current: {realtime['generator']['current']} A", format="%.2f")
                        tgb.text("Power: {realtime['generator']['power']} W")

                tgb.text("#### ⚡️ Grid", mode="md")
                with tgb.layout("1fr 3fr", gap="20px", class_name="container align_columns_center"):
                    tgb.part()
                    with tgb.part():
                        tgb.text("Voltage: {realtime['grid']['voltage']} V", format="%.1f")
                        tgb.text("Current: {realtime['grid']['current']} A", format="%.2f")

                tgb.text("#### 🔋 Production", mode="md")
                with tgb.layout("1fr 3fr", gap="20px", class_name="container align_columns_center"):
                    tgb.part()
                    with tgb.part():
                        tgb.text("Delivered: {realtime['production']['power']} W")
                        tgb.text("Yeld: {realtime['production']['yeld']} W")

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
        global daily_stats, monthly_stats, yearly_stats
        # Read config
        #mylib.config_dbfile
        while True:
            #value = f"{random.uniform(1000, 5000):.2f}"
            #daily_stats["Power"].append(value)
            #daily_stats["Time"].append(len(daily_stats["Power"]))
            daily_stats=db.pread_daily_details(mylib.datestamp())
            monthly_stats=db.pread_monthly_stats(mylib.datestamp())
            yearly_stats=db.pread_yearly_stats(mylib.datestamp())

            if hasattr(self.gui, "_server") and state_id:
                invoke_callback(self.gui, state_id, update_value) #, (value,))
            time.sleep(delay)

# Get the state id
def on_init(state: State):
    global state_id
    state_id = get_state_id(state)

# Update the value within the state
def update_value(state: State):
    #state.realtime["generator"]["power"] = daily_stats["Power"][len(daily_stats["Power"])-1]
    #state.realtime["generator"]["voltage"] = random.uniform(200, 250)
    state.daily_stats = daily_stats
    state.monthly_stats = monthly_stats

if __name__ == "__main__":
    # Create the gui object (here because needed by the read thread)
    gui = Gui(create_page())

    # Start reader thread
    read(gui).start()

    # Start webui
    gui.run(title="PVM", favicon="favicon.ico", single_client=True, host="0.0.0.0", port=9000)

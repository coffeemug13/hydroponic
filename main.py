"""
sudo systemctl start hydro.service
sudo systemctl enable hydro.service
"""
import time
import datetime as dt
import signal
import logging

#from switches import Switches
from switches_gpio import Switches

"""
Configuration
"""
SECONDS_PER_DAY = 86400

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='hydro: %(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )
_LOGGER = logging.getLogger(__name__)

_LOGGER.info("Starting Hydroponic Server v0.1")

schedules = {"1": {"switch": "A", "on": 60*2, "off": 60*20, "status": 0, "next-on": 0, "next-off": 0},
             "2": {"switch": "B", "on": 60 * 10, "off": int(SECONDS_PER_DAY / 4), "status": 0, "next-on": 0,
                   "next-off": 0}}

"""
Init the system
"""
switches = Switches()
switches.all_off()
switches.on("A")
time.sleep(1)
switches.all_off()

now = dt.datetime.today()
today = dt.datetime.combine(now, dt.time.min)
tomorrow = today + dt.timedelta(days=1)

now = int(now.timestamp())
today = int(today.timestamp())
tomorrow = int(tomorrow.timestamp())

_LOGGER.info(str(dt.datetime.fromtimestamp(now)) + " - " + str(now))
#today = int(now / SECONDS_PER_DAY) * SECONDS_PER_DAY  # seconds of today 00:00:00
_LOGGER.info(str(dt.datetime.fromtimestamp(today)) + " - " + str(today))
#tomorrow = today + SECONDS_PER_DAY  # seconds of tomorrow 00:00:00
_LOGGER.info(str(dt.datetime.fromtimestamp(tomorrow)) + " - " + str(tomorrow))

class GracefulKiller:
    """
    https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
    """
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True
        _LOGGER.info("got the signal to shutdown")

"""
Run the system
"""
if __name__ == '__main__':
    # init the schedules like they started with 00:00:00 of this day
    for sid, schedule in schedules.items():
        interval = schedule["on"] + schedule["off"]  # seconds of one interval
        delta = now - today  # seconds of this day since 00:00:00
        number_of_intervals = int(delta / interval)
        schedule["next-on"] = today + (number_of_intervals + 1) * interval  # we skip to the next full interval
        print(str(schedule["next-on"] - tomorrow))
        if schedule["next-on"] > tomorrow:
            schedule["next-on"] = tomorrow
        date_time = str(dt.datetime.fromtimestamp(schedule["next-on"]))
        _LOGGER.info("start switch " + schedule["switch"] + " at: " + date_time + "/" + str(schedule["next-on"]))

    # now run the schedules
    killer = GracefulKiller()
    while not killer.kill_now:
        now = int(dt.datetime.today().timestamp())
        # reset clocks
        for sid, schedule in schedules.items():
            if schedule["next-on"] < now and schedule["status"] == 0:
                # Time to start a new period
                schedule["status"] = 1
                schedule["next-on"] = now + schedule["on"] + schedule["off"]
                schedule["next-off"] = now + schedule["on"]
                switches.on(schedule["switch"])
                _LOGGER.debug("switch off at: " + str(dt.datetime.fromtimestamp(schedule["next-off"])))
            elif schedule["next-off"] < now and schedule["status"] == 1:
                # Time to stop
                schedule["status"] = 0
                switches.off(schedule["switch"])
            else:
                if _LOGGER.isEnabledFor(logging.DEBUG):
                    print(".", end="")
        time.sleep(1.0)

    switches.all_off()
    _LOGGER.info("Hydroponic Server shutdown")

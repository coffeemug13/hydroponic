"""
scp switches* pi@192.168.112.193:./script/
"""
import logging
from rpi_rf import RFDevice

_LOGGER = logging.getLogger(__name__)

GPIO = 17


class Switches:
    def __init__(self):
        self.rfdevice = RFDevice(gpio=GPIO)
        self.switches = {"A":[1377620,1377617],
                         "B":[1380692,1380689]}

    def _send(self, code):
        self.rfdevice.enable_tx()
        self.rfdevice.tx_code(code=code)

    def on(self, switch: str):
        _LOGGER.info("switch on:" + switch)
        self._send(self.switches[switch][1])

    def off(self, switch: str):
        _LOGGER.info("switch off:" + switch)
        self._send(self.switches[switch][0])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rfdevice.cleanup()

    def all_off(self):
        for switch,interval in self.switches.items():
            self.off(switch)

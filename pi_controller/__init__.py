import time

import board
import neopixel

from ..data_controller import METARData, Colors


TOTAL_LIGHTS = 300

class RunLights:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, TOTAL_LIGHTS, brightness=.05, pixel_order=neopixel.RGB)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.pixels.deinit()

    def refresh(self, interval):
        try:
            metar = METARData()
            data = metar.pull_metar_data()
            with open(metar.station_data, 'r') as f:
                for i, station in enumerate(f.readlines()):
                    self.pixels[i] = data.get(station.strip(), Colors.COLOR_CLEAR.value)
                    if i + 1 == TOTAL_LIGHTS:
                        break
            self.pixels[273] = Colors.VFR.value
            self.pixels[274] = Colors.MVFR.value
            self.pixels[275] = Colors.IFR.value
            self.pixels[276] = Colors.LIFR.value
            self.pixels.show()
        except Exception:
            pass
        time.sleep(interval * 60)

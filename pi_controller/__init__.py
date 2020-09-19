import time

import board
import neopixel

from ..data_controller import METARData, Colors


TOTAL_LIGHTS = 250

class RunLights:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, TOTAL_LIGHTS, brightness=.5, pixel_order=neopixel.RGB)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.pixels.deinit()

    def refresh(self, interval):
        metar = METARData()
        data = metar.pull_metar_data()
        with open(metar.station_data, 'r') as f:
            for i, station in enumerate(f.readlines()):
                self.pixels[i] = data.get(station.strip(), Colors.COLOR_CLEAR.value)
                if i + 1 == TOTAL_LIGHTS:
                    break
        self.pixels.show()
        time.sleep(interval)

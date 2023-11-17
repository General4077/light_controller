from data_controller import METARData
from pprint import pprint

if __name__ == '__main__':
    metar = METARData()
    pprint(metar.pull_metar_data())

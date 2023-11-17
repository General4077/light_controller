from requests import get
from bs4 import BeautifulSoup as Soup
from enum import Enum
import os
from pathlib import Path


class Colors(Enum):
    VFR = (0, 255, 0)
    MVFR = (0, 0, 255)
    IFR = (255, 0, 0)
    LIFR = (125, 0, 125)
    COLOR_CLEAR = (0, 0, 0)
    WHITE = (255, 255, 255) # Troubleshooting


class METARData:

    url :str = "https://aviationweather.gov/api/data/dataserver"

    @property
    def station_data(self):
        p = Path('.')
        if Path('light_controller').exists():
            return p / 'light_controller' / 'stations.data'
        elif Path('stations.data').exists():
            return p / 'stations.data'
        else:
            raise FileNotFoundError('Could not find stations.data file')

    @property
    def stations(self):
        with open(self.station_data, 'r') as f:
            return [line.strip() for line in f.readlines()]

    @property
    def url_params(self):
        return {
            'dataSource': 'metars',
            'requestType': 'retrieve',
            'format': 'xml',
            'hoursBeforeNow': '5',
            'mostRecentForEachStation': 'constraint',
            'stationString': ','.join(self.stations)
        }


    def _request_metar_data(self):
        r = get(self.url, params = self.url_params.items())
        return r.content.decode('utf-8', errors='replace')


    def _parse_metar_data(self, data: str) -> dict:
        soup = Soup(data, features="html.parser")
        data = dict()
        for ele in soup.find_all('metar'):
            station = ele.find('station_id').get_text().strip()
            flight_cat = ele.find('flight_category').get_text() if ele.find('flight_category') else 'None'
            station_stat = getattr(Colors, flight_cat, Colors.COLOR_CLEAR)
            data[station] = station_stat.value
        return data



    def pull_metar_data(self):
        data = self._request_metar_data()
        return self._parse_metar_data(data)

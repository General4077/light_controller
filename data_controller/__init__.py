from requests import get
from bs4 import BeautifulSoup as Soup
from enum import Enum
import os

class Colors(Enum):
    VFR = (0, 255, 0)
    MVFR = (0, 0, 255)
    IFR = (255, 0, 0)
    LIFR = (125, 0, 125)
    COLOR_CLEAR = (0, 0, 0)


class METARData:

    @property
    def station_data(self):
        return os.path.join('light_controller', 'stations.data')

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
            'mostRecentForEachStation': 'true',
            'fields': 'flight_category,station_id',
            'stationString': ' '.join(self.stations)
        }

    @property
    def url(self):
        _url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?"
        return _url + '&'.join([f'{k}={v}' for k, v in self.url_params.items()])



    def _request_metar_data(self):
        r = get(self.url)
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

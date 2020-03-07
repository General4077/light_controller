from requests import get
from bs4 import BeautifulSoup as Soup
from enum import Enum
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class Colors(Enum):
    VFR = (255, 0, 0)
    MVFR = (0, 0, 255)
    IFR = (0, 255, 0)
    LIFR = (0, 125, 125)
    COLOR_CLEAR = (0, 0, 0)



stations = {
    'KBOS': 1,
    'KATL': 0,
    'KBWI': 10,
    'KCLE': 15,
    'KCLT': 23,
    'KCVG': 36,
    'CWOB': 45,
    'CYTE': 50
}

# COLOR_VFR = (255, 0, 0)				# Green
# COLOR_MVFR = (0, 0, 255)				# Blue
# COLOR_IFR = (0, 255, 0)				# Red
# COLOR_LIFR = (0, 125, 125)			# Magenta


def _request_metar_data():
    url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&"
    url = url + '&'.join(
        [
            'requestType=retrieve',
            'format=xml&hoursBeforeNow=5',
            'mostRecentForEachStation=true',
            'fields=flight_category,station_id',
            'stationString=' + ','.join(stations.keys())
        ]
    )
    r = get(url)
    return r.content.decode('utf-8', errors='replace')


def _parse_metar_data(data: str) -> dict:
    soup = Soup(data)
    data = dict()
    for ele in soup.find_all('metar'):
        station = ele.find('station_id').get_text().strip()
        flight_cat = ele.find('flight_category').get_text() if ele.find('flight_category') else 'None'
        station_stat = getattr(Colors, flight_cat, Colors.COLOR_CLEAR)
        logger.info(f"{station}: {station_stat:>8}")
        data[station] = station_stat.value
    return data



def pull_metar_data():
    data = _request_metar_data()
    logger.info(data)
    return _parse_metar_data(data)


if __name__ == '__main__':
    print(Colors.VFR.value)
    with open('test.data', 'r') as f:
        print(_parse_metar_data(f.read()))

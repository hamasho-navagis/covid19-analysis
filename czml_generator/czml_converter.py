import datetime
import json
from lib import PROJ_DIR
from data import get_world_accum_cases


COVID19_CZML_PATH = f'{PROJ_DIR}/datasets/' \
    + 'COVID-19-geographic-disbtribution-worldwide-2020-03-19-latlon.czml'


def column2id(col):
    id = col['Country/Region']
    if s := col['Province/State']:
        id = f'{id}--{s}'
    return f'{id}-{col["Date"].isoformat()}'


def isodate(d, end=False):
    '''Convert date to ISO-8601 format

    >>> from datetime import date, datetime
    >>> isodate(date(2010, 1, 1))
    '2010-01-01T00:00:00Z'
    >>> isodate(datetime(2010, 1, 1))
    '2010-01-01T00:00:00Z'
    >>> isodate(date(2010, 1, 1), end=True)
    '2010-01-01T23:59:59Z'
    '''
    if isinstance(d, datetime.datetime):
        d = d.date()
    d = d.isoformat()
    return f'{d}T23:59:59Z' if end else f'{d}T00:00:00Z'


def column2packet(col):
    avail = f'{isodate(col["Date"])}/{isodate(col["Date"], end=True)}'
    axis = col['Axis']
    packet = {
        'id': column2id(col),
        'availability': avail,
        'position': {
            'cartographicDegrees': [col['Long'], col['Lat'], 1000000],
        },
        'ellipse': {
            'semiMinorAxis': axis,
            'semiMajorAxis': axis,
            'material': {
                'solidColor': {
                    'color': {
                        'rgba': [255, 0, 0, 60]
                    }
                }
            },
        },
    }
    return packet


def set_axis(df):
    '''Set Cesium's axis 0 or 5000 ~ 100000'''
    max_axis = 800000
    min_axis = 70000
    conf_max = df['Confirmed'].max()
    def axis(conf):
        if conf == 0:
            return 0
        return min_axis + (max_axis - min_axis) * conf / conf_max

    df['Axis'] = df['Confirmed'].apply(axis)


def convert_covid19_to_czml():
    df = get_world_accum_cases()
    #df = df[df['Date'] > '2020-03-01']
    set_axis(df)
    doc = [{
        'id': 'document',
        'name': 'COVID-19',
        'version': '1.0',
        'clock': {
            'interval': None,
            'currentTime': None,
            'multiplier':  10 * 3600 * 24,
            'range': 'LOOP_STOP',
            'step': 'SYSTEM_CLOCK_MULTIPLIER',
        },
    }]
    df = df[df['Axis'] > 0]
    packets = [column2packet(d) for _, d in df.iterrows()]
    doc += packets
    start = min(df['Date'])
    end = max(df['Date'])
    doc[0]['clock']['interval'] = f'{isodate(start)}/{isodate(end)}'
    doc[0]['clock']['currentTime'] = isodate(datetime.date(2020, 3, 3))

    print(max([p['ellipse']['semiMinorAxis'] for p in packets[1:]]))

    with open(COVID19_CZML_PATH, 'w') as f:
        f.write(json.dumps(doc, indent=2))


if __name__ == "__main__":
    convert_covid19_to_czml()

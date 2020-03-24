import json
from lib import PROJ_DIR
from data import get_world_accum_cases


COVID19_CZML_PATH = f'{PROJ_DIR}/datasets/' \
    + 'COVID-19-geographic-disbtribution-worldwide-2020-03-19-latlon.czml'


def column2id(col):
    id = col['Country/Region']
    if s := col['Province/State']:
        id = f'{id} - {s}'
    return f'{id}-{col["Date"].isoformat()}'


def isodate(d, end=False):
    '''Convert date to ISO-8601 format

    >>> from datetime import date
    >>> isodate(date(2010, 1, 1))
    '2010-01-01T00:00:00Z'
    >>> isodate(date(2010, 1, 1), end=True)
    '2010-01-01T23:59:59Z'
    '''
    d = d.isoformat()
    return f'{d}T23:59:59Z' if end else f'{d}T00:00:00Z'


def column2packet(col):
    avail = f'{isodate(col["Date"])}/{isodate(col["Date"], end=True)}'
    axis = 250000 * 1
    packet = {
        'id': column2id(col),
        'availability': avail,
        'position': {
            'cartographicDegrees': [col['Long'], col['Lat'], 1000000],
        },
        'ellipse': {
            'semiMinorAxis': axis,
            'semiMajorAxis': axis,
            'fill': True,
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


def convert_covid19_to_czml():
    df = get_world_accum_cases()
    doc = [{
        'id': 'document',
        'name': 'COVID-19',
        'version': '1.0',
        'clock': {
            'interval': None,
            'currentTime': None,
            'multiplier':  3600 * 24,
            'range': 'LOOP_STOP',
            'step': 'SYSTEM_CLOCK_MULTIPLIER',
        },
    }]
    packets = [column2packet(d) for _, d in df.iterrows()]
    doc += packets
    start = min(df['Date'])
    end = max(df['Date'])
    doc[0]['clock']['interval'] = f'{isodate(start)}/{isodate(end)}'
    doc[0]['clock']['currentTime'] = isodate(start)

    with open(COVID19_CZML_PATH, 'w') as f:
        f.write(json.dumps(doc, indent=2))

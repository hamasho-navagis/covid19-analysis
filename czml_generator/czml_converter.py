import json
from lib import PROJ_DIR, line2record


COVID19_PATH = f'{PROJ_DIR}/datasets/' \
    + 'COVID-19-geographic-disbtribution-worldwide-2020-03-19-latlon.csv'
COVID19_CZML_PATH = f'{PROJ_DIR}/datasets/' \
    + 'COVID-19-geographic-disbtribution-worldwide-2020-03-19-latlon.czml'


def record2id(rec):
    return f'{rec.country_code}-{rec.date.isoformat()}'


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


def record2packet(rec):
    avail = f'{isodate(rec.date)}/{isodate(rec.date, end=True)}'
    axis = 250000 * 1
    packet = {
        'id': record2id(rec),
        'availability': avail,
        'position': {
            'cartographicDegrees': [rec.lng, rec.lat, 1000000],
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
    with open(COVID19_PATH) as f:
        data = f.read()
    data = data.splitlines()[1:]
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
    records = [line2record(d) for d in data]
    dates = set()
    for rec in records:
        dates.add(rec.date)
        doc.append(record2packet(rec))
    start = min(dates)
    end = max(dates)
    max_cases = max([r.cases for r in records])
    print(max_cases)
    doc[0]['clock']['interval'] = f'{isodate(start)}/{isodate(end)}'
    doc[0]['clock']['currentTime'] = isodate(start)

    with open(COVID19_CZML_PATH, 'w') as f:
        f.write(json.dumps(doc, indent=2))

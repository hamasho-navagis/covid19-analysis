import json
import os


DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def cc2ll(cc):
    '''Convert Country CODE (e.g. AF, JP) to (LAT, LNG) tuple

    >>> cc2ll('AF')
    (33.0, 65.0)
    >>> cc2ll('JP')
    (36.0, 138.0)
    >>> cc2ll('us')
    (38.0, -97.0)
    '''
    cc = cc.lower()
    with open(f'{DIR}/countrycode-latlong-array.json') as f:
        data = json.loads(f.read())
        lat, lng = data[cc]
        return (float(lat), float(lng))

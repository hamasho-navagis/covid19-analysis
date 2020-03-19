import json
import os


PY_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
PROJ_DIR = os.path.dirname(PY_DIR)


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
    with open(f'{PY_DIR}/countrycode-latlong-array.json') as f:
        data = json.loads(f.read())
        lat, lng = data[cc]
        return (float(lat), float(lng))


def add_lat_lng(csv_content):
    '''Add LNG/LAT column to CSV string

    >>> test_csv = """
    ... DateRep,Day,Month,Year,Cases,Deaths,Countries and territories,GeoId
    ... 3/19/2020,19,3,2020,0,0,Afghanistan,AF
    ... 3/18/2020,18,3,2020,1,0,Afghanistan,AF
    ... """
    >>> print(add_lat_lng(test_csv))
    DateRep,Day,Month,Year,Cases,Deaths,Countries and territories,GeoId,Lat,Lng
    3/19/2020,19,3,2020,0,0,Afghanistan,AF,33.00,65.00
    3/18/2020,18,3,2020,1,0,Afghanistan,AF,33.00,65.00
    <BLANKLINE>
    '''

    def add_ll(line):
        cols = line.split(',')
        ll = cc2ll(cols[-1])
        return f'{line},{ll[0]:.2f},{ll[1]:.2f}'

    lines = csv_content.splitlines()
    lines = lines[1:]  # ignore first emply line
    result = [lines[0] + ',Lat,Lng'] + [add_ll(l) for l in lines[1:]]
    return '\n'.join(result) + '\n'


def add_lat_lng_col_to_file(src, dist):
    if os.path.exists(dist):
        print(f'already exists: {dist}')
        return
    with open(src) as src_file:
        content = src_file.read()
    new_content = add_lat_lng(content)
    with open(dist, 'w') as dist_file:
        dist_file.write(new_content)

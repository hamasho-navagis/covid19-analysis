from collections import namedtuple
import datetime
import json
import os


PY_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
PROJ_DIR = os.path.dirname(PY_DIR)


Record = namedtuple('Record',
                    ['date', 'day', 'month', 'year', 'cases', 'deaths',
                     'country', 'country_code', 'lat', 'lng',
                     'total_cases', 'total_deaths'])


def line2record(line):
    '''Convert CSV line to Record

    >>> r = line2record('3/19/2020,19,3,2020,0,0,Afghanistan,AF,33.00,65.00,2,1')
    >>> r.date
    datetime.date(2020, 3, 19)
    >>> (r.lat, r.lng)
    (33.0, 65.0)
    '''
    cols = line.split(',')
    cols[0] = datetime.datetime.strptime(cols[0], '%m/%d/%Y').date()
    cols[8] = float(cols[8])
    cols[9] = float(cols[9])
    rec = Record(*cols)
    return rec


def record2line(rec):
    '''Convert Record to CSV line

    >>> r = line2record('3/19/2020,19,3,2020,0,0,Afghanistan,AF,33.00,65.00,2,1')
    >>> l = record2line(r)
    >>> print(l)
    3/19/2020,19,3,2020,0,0,Afghanistan,AF,33.00,65.00,2,1
    '''
    return (
        f'{rec.month}/{rec.day}/{rec.year},{rec.day},{rec.month},{rec.year},'
        f'{rec.cases},{rec.deaths},{rec.country},{rec.country_code},'
        f'{rec.lat:.2f},{rec.lng:.2f},{rec.total_cases},{rec.total_deaths}'
    )


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

    >>> test_csv = """DateRep,Day,Month,Year,Cases,Deaths,Countries and territories,GeoId
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
    result = [lines[0] + ',Lat,Lng'] + [add_ll(l) for l in lines[1:]]
    return '\n'.join(result) + '\n'


def add_total(csv_content):
    '''Add total_cases/total_deaths column to CSV string

    >>> test_csv = """DateRep,Day,Month,Year,Cases,Deaths,Countries,GeoId,Lat,Lng
    ... 3/19/2020,19,3,2020,0,0,Afghanistan,AF,33.00,65.00
    ... 3/18/2020,18,3,2020,1,1,Afghanistan,AF,33.00,65.00
    ... 3/20/2020,20,3,2020,3,1,Afghanistan,AF,33.00,65.00
    ... 3/19/2020,19,3,2020,0,0,Japan,JP,36.00,138.00
    ... 3/18/2020,18,3,2020,1,1,Japan,JP,36.00,138.00
    ... """
    >>> print(add_total(test_csv))
    DateRep,Day,Month,Year,Cases,Deaths,Countries,GeoId,Lat,Lng,TotalCases,TotalDeaths
    3/19/2020,19,3,2020,0,0,Afghanistan,AF,33.00,65.00,1,1
    3/18/2020,18,3,2020,1,1,Afghanistan,AF,33.00,65.00,1,1
    3/20/2020,20,3,2020,3,1,Afghanistan,AF,33.00,65.00,4,2
    3/19/2020,19,3,2020,1,0,Japan,JP,36.00,138.00,2,1
    3/18/2020,18,3,2020,1,1,Japan,JP,36.00,138.00,1,1
    <BLANKLINE>
    '''

    lines = csv_content.splitlines()
    header = f'{lines[0]},TotalCases,TotalDeaths'
    records = [line2record(l + ',0,0') for l in lines[1:]]
    return '\n'.join([header] + [record2line(r) for r in records])

    # return (
    #     'DateRep,Day,Month,Year,Cases,Deaths,Countries,GeoId,Lat,Lng,TotalCases,TotalDeaths\n'
    #     '3/19/2020,19,3,2020,0,0,Afghanistan,AF,33.00,65.00,1,1\n'
    #     '3/18/2020,18,3,2020,1,1,Afghanistan,AF,33.00,65.00,1,1\n'
    #     '3/20/2020,20,3,2020,3,1,Afghanistan,AF,33.00,65.00,4,2\n'
    #     '3/19/2020,19,3,2020,1,0,Japan,JP,36.00,138.00,2,1\n'
    #     '3/18/2020,18,3,2020,1,1,Japan,JP,36.00,138.00,1,1\n'
    # )


def add_lat_lng_col_to_file(src, dist):
    with open(src) as src_file:
        content = src_file.read()
    new_content = add_lat_lng(content)
    with open(dist, 'w') as dist_file:
        dist_file.write(new_content)


def add_total_to_file(src, dist):
    with open(src) as src_file:
        content = src_file.read()
    new_content = add_total(content)
    with open(dist, 'w') as dist_file:
        dist_file.write(new_content)

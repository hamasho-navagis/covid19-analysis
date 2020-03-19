import json
import os
import numpy as np
import pandas as pd


PY_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
PROJ_DIR = os.path.dirname(PY_DIR)

'''Dataset downloaded from Europian research center
Header: DateRep,Day,Month,Year,Cases,Deaths,Countries and territories,GeoId
'''
RAW_DS_PATH = f'{PROJ_DIR}/datasets/COVID-19-geographic-disbtribution-worldwide-2020-03-19.csv'
'''Add Lat/Long/TotalCases/TotalDeaths'''
NEW_DS_PATH = f'{PROJ_DIR}/datasets/COVID-19-full.csv'


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


def convert_data():
    df = pd.read_csv(RAW_DS_PATH, keep_default_na=False)  # avoid converting NA to NaN

    df['DateRep'] = pd.to_datetime(df['DateRep'], format='%m/%d/%Y')
    df = df.sort_values(by=['GeoId', 'DateRep'])
    loc = np.vectorize(cc2ll)(df['GeoId'])
    df['Lat'] = loc[0]
    df['Long'] = loc[1]
    df['TotalCases'] = df.groupby(by=['DateRep', 'GeoId'])['Cases'].apply(lambda x: x.cumsum())
    df['TotalDeaths'] = df.groupby(by=['DateRep', 'GeoId'])['Deaths'].apply(lambda x: x.cumsum())

    df.to_csv(NEW_DS_PATH, index=False)


if __name__ == "__main__":
    convert_data()

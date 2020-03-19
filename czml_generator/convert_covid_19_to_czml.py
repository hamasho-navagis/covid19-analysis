from lib import PROJ_DIR, add_lat_lng_col_to_file
from czml_converter import convert_covid19_to_czml


def _add_lat_lng():
    src = f'{PROJ_DIR}/datasets/COVID-19-geographic-disbtribution-worldwide-2020-03-19.csv'
    dist = f'{PROJ_DIR}/datasets/COVID-19-geographic-disbtribution-worldwide-2020-03-19-latlon.csv'
    add_lat_lng_col_to_file(src, dist)


if __name__ == "__main__":
    # convert_covid19_to_czml()
    _add_lat_lng()

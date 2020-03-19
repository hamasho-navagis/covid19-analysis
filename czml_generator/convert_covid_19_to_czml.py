from lib import cc2ll, PROJ_DIR, add_lat_lng_col_to_file


def convert_covid_file():
    src = f'{PROJ_DIR}/datasets/COVID-19-geographic-disbtribution-worldwide-2020-03-19.csv'
    dist = f'{PROJ_DIR}/datasets/COVID-19-geographic-disbtribution-worldwide-2020-03-19-latlon.csv'
    add_lat_lng_col_to_file(src, dist)


if __name__ == "__main__":
    convert_covid_file()

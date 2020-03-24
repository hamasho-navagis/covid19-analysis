import pandas as pd
from lib import DS_PATH


def load_full_df():
    full_table = pd.read_csv(f'{DS_PATH}/covid_19_clean_complete.csv',
                             parse_dates=['Date'])

    # replacing Mainland china with just China
    full_table['Country/Region'] = \
        full_table['Country/Region'].replace('Mainland China', 'China')
    # filling missing values with NA
    full_table[['Province/State']
               ] = full_table[['Province/State']].fillna('NA')

    # cases in the Diamond Princess cruise ship
    ship = full_table[full_table['Province/State']
                      == 'Diamond Princess cruise ship']
    full_table = full_table[full_table['Province/State']
                            != 'Diamond Princess cruise ship']
    china = full_table[full_table['Country/Region'] == 'China']
    row = full_table[full_table['Country/Region'] != 'China']

    full_latest = full_table[full_table['Date']
                             == max(full_table['Date'])].reset_index()
    china_latest = full_latest[full_latest['Country/Region'] == 'China']
    row_latest = full_latest[full_latest['Country/Region'] != 'China']

    full_latest_grouped = full_latest.groupby(
        'Country/Region')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()
    china_latest_grouped = china_latest.groupby(
        'Province/State')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()
    row_latest_grouped = row_latest.groupby(
        'Country/Region')['Confirmed', 'Deaths', 'Recovered'].sum().reset_index()

    return dict(
        full_table=full_table,
        ship=ship,
        china=china,
        row=row,
        full_latest=full_latest,
        china_latest=china_latest,
        row_latest=row_latest,
        full_latest_grouped=full_latest_grouped,
        china_latest_grouped=china_latest_grouped,
        row_latest_grouped=row_latest_grouped,
    )


def get_world_accum_cases():
    full = TABLES['full_table']
    df = full.groupby(['Date', 'Country/Region', 'Province/State']
                      )['Confirmed', 'Deaths', 'Recovered', 'Lat', 'Long'].max()
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    return df


TABLES = load_full_df()

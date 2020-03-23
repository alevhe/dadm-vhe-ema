import pandas as pd
import dateutil.parser


def _read_file(filename):
    df = pd.read_csv(filename)

    df = df.drop('id', axis=1)

    return df


def _split_dates(df):
    dates = df['date'].apply(dateutil.parser.parse)

    df['year'] = dates.apply(lambda d: d.year)
    df['month'] = dates.apply(lambda d: d.month)
    df['day'] = dates.apply(lambda d: d.day)

    df = df.drop('date', axis=1)

    return df


def _zip_encode(df):
    zip_ohe = pd.get_dummies(df['zipcode'], prefix='zip')

    df.drop('zipcode', axis=1)

    df = pd.concat([df, zip_ohe], axis=1)

    return df


def get_dataset(filename='data/kc_house_data.csv'):
    df = _read_file(filename)

    df = _split_dates(df)
    df = _zip_encode(df)

    return df
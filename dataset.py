import pandas as pd
import dateutil.parser


def _read_file(filename):
    df = pd.read_csv(filename)
    df = df.drop('Id', axis=1)
    return df

def _split_dates(df):
    MSZonind_dict =  {'A': 0, 'C (all)': 1, 'C': 1, 'FV': 2, 'I': 3, 'RH': 4, 'RL': 5, 'RP': 6, 'RM': 7}
    df['MSZoning'] = df['MSZoning'].replace(to_replace=MSZonind_dict)
    return df


def _zip_encode(df):
    zip_ohe = pd.get_dummies(df['zipcode'], prefix='zip')

    df.drop('zipcode', axis=1)

    df = pd.concat([df, zip_ohe], axis=1)

    return df


def get_dataset(filename='data/train.csv'):
    df = _read_file(filename)

    df = _split_dates(df)
    df = _zip_encode(df)

    return df
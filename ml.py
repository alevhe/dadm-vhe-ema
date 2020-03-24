import numpy as np
from time import time
import pandas as pd

from sklearn.model_selection import train_test_split, ParameterGrid, GridSearchCV, KFold
from sklearn.preprocessing import normalize
from sklearn import preprocessing


def prepare_dataset(df, y_col, ts_size=0.33):
    x_first = df.loc[:, df.columns != y_col]
    y = df[y_col]

#    dfn = normalize(x_first, axis=0)
#    x = pd.DataFrame(dfn, columns=x_first.columns)

    val = x_first.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(val)
    df = pd.DataFrame(x_scaled)

    x = df
    xtr, xts, ytr, yts = train_test_split(x, y, test_size=ts_size, shuffle=True)

    return xtr, xts, ytr, yts


def train_estimator(estimator, xtr, ytr, params={}, folds=2):
    cv = KFold(n_splits=folds)

    clf = GridSearchCV(estimator, params, cv=cv, return_train_score=True, n_jobs=4)

    clf.fit(xtr, ytr)

    return clf


def test_estimator(clf, xts, yts):
    df = pd.DataFrame(clf.cv_results_)
#    df = df.filter(regex='^mean.*score$|^std.*score$|^param_')
    df = df.filter(regex='^mean.*score$|^param_')

    #df = df.sort_values('mean_test_score', ascending=False)
    """
    print(" Results: ")
    print(df.iloc[:])
    print("Best params: ")
    print(clf.best_params_)
    print("Best score: ")
    print(clf.best_score_)
    """
    return df

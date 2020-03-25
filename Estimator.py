import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn import preprocessing

def normalize_set(df, y_col, ts_size):
    x_first = df.loc[:, df.columns != y_col]
    y = df[y_col]
    val = x_first.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(val)
    x = pd.DataFrame(x_scaled)
    xtr, xts, ytr, yts = train_test_split(x, y, test_size=ts_size, shuffle=True)
    return xtr, xts, ytr, yts


def train_estimator(estimator, xtr, ytr, params, folds):
    cv = KFold(n_splits=folds)
    clf = GridSearchCV(estimator, params, cv=cv, return_train_score=True, n_jobs=4)
    clf.fit(xtr, ytr)
    return clf


def test_estimator(clf, xts, yts):
    df = pd.DataFrame(clf.cv_results_)
    df = df.filter(regex='^mean.*score$|^param_')
    RESU = [clf.score(xts, yts), clf.best_params_]
    return df, RESU

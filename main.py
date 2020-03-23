from sys import stderr
from numpy import logspace

import pandas as pd

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge

import dataset
import ml


def debug(*args):
    print('\033[35m', *args, '\033[m', file=stderr)


def main(params_no=2, folds=2, limit=100000, show_stats=False):
    debug('Reading dataset...')
    df = dataset.get_dataset().iloc[:limit]
    debug('Preparing dataset...')
    xtr, xts, ytr, yts = ml.prepare_dataset(df, 'price', ts_size=0.33)

    rls_params = {'alpha': logspace(-3, 2, params_no)}
    krls_params = {
        'kernel': [
            'rbf',
            'poly',
            'laplacian'
        ],
        'alpha': logspace(-3, 2, params_no),
        'gamma': logspace(-3, 2, params_no)
    }
    debug('Training LS...')
    ls = ml.train_estimator(LinearRegression(), xtr, ytr, folds=folds)
    debug('Training RLS...')
    rls = ml.train_estimator(Ridge(solver='svd'), xtr, ytr, rls_params, folds=folds)
    debug('Training KRLS...')
    krls = ml.train_estimator(KernelRidge(), xtr, ytr, krls_params, folds=folds)

    debug('Testing LS...')
    ls_score = ml.test_estimator(ls, xts, yts, show_stats=show_stats)
    debug('Testing RLS...')
    rls_score = ml.test_estimator(rls, xts, yts, show_stats=show_stats)
    debug('Testing KRLS...')
    krls_score = ml.test_estimator(krls, xts, yts, show_stats=show_stats)

    print('  LS:', ls_score)
    print(' RLS:', rls_score)
    print('KRLS:', krls_score)
    
    return ls, rls, krls


if __name__ == '__main__':
    main(params_no=2, folds=2, limit=1000)
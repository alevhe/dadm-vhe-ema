from sklearn import preprocessing
from numpy import logspace
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge

import DatasetPreparation
import Estimator

if __name__ == '__main__':
    #initialize the params
    input_filename = 'data/train.csv'#name of the fail to be trained
    test_filename = 'data/test.csv'  # name of the fail to be trained
    y_column = 'SalePrice' #label of the results column
    withLS = False
    withRLS = True
    withKRLS = True
    folds = 3
    rls_n_lambda_to_try = 8  # number of lambda to try
    rls_min_lambda = -3  # exponent of 10, is the minimum value of lambda to try
    rls_max_lambda = 1  # exponent of 10, is the maximum value of lambda to try
    kernel_list = ['rbf', 'poly', 'laplacian']  # list of the kernel to be used
    krls_n_lambda_to_try = 8  # number of lambda to try
    krls_min_lambda = -3  # exponent of 10, is the minimum value of lambda to try
    krls_max_lambda = 1  # exponent of 10, is the maximum value of lambda to try
    krls_n_gamma_to_try = 8  # number of gamma to try
    krls_min_gamma = -3  # exponent of 10, is the minimum value of gamma to try
    krls_max_gamma = 1  # exponent of 10, is the maximum value of gamma to try

    #read the dataset only the first time (I doesn't change)
    print('Reading dataset...')
    input = DatasetPreparation._read_file(input_filename)
    test = DatasetPreparation._read_file(test_filename)
    # obtain 4 different matrix (x-train, x-test, y-train, y-test)
    xtr = input.loc[:, input.columns != y_column]
    ytr = input[y_column]

    val = xtr.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(val)
    xtr = pd.DataFrame(x_scaled)

    val_test = test.values
    min_max_scaler_test = preprocessing.MinMaxScaler()
    test_scaled = min_max_scaler_test.fit_transform(val_test)
    test = pd.DataFrame(test_scaled)

    if withLS:
        ls = Estimator.train_estimator(LinearRegression(), xtr, ytr, params={}, folds=folds)
        ls_result = ls.predict(test)
    if withRLS:
        rls_params = {'alpha': logspace(rls_min_lambda, rls_max_lambda, rls_n_lambda_to_try)}
        rls = Estimator.train_estimator(Ridge(solver='auto'), xtr, ytr, rls_params, folds=folds)
        rls_result = rls.predict(test)
    if withKRLS:
        krls_params = {
            'kernel': kernel_list,
            'alpha': logspace(krls_min_lambda, krls_max_lambda, krls_n_lambda_to_try),
            'gamma': logspace(krls_min_gamma, krls_max_gamma, krls_n_gamma_to_try)
        }
        ls = Estimator.train_estimator(LinearRegression(), xtr, ytr, params={}, folds=folds)
        krls = Estimator.train_estimator(KernelRidge(), xtr, ytr, krls_params, folds=folds)
        krl_result = krls.predict(test)

from sklearn import preprocessing
from numpy import logspace
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.preprocessing import normalize
import DataPreProccesingCat
import Estimator

if __name__ == '__main__':
    #initialize the params
    input_filename = 'data/train.csv'#name of the fail to be trained
    test_filename = 'data/test.csv'  # name of the fail to be trained
    y_column = 'SalePrice' #label of the results column
    withLS = False
    withRLS = False
    withKRLS = True
    l2 = True  # if to normalize with l2
    folds = 3
    rls_n_lambda_to_try = 8  # number of lambda to try
    rls_min_lambda = -2  # exponent of 10, is the minimum value of lambda to try
    rls_max_lambda = 1  # exponent of 10, is the maximum value of lambda to try
    kernel_list = ['laplacian']  # list of the kernel to be used
    krls_n_lambda_to_try = 10  # number of lambda to try
    krls_min_lambda = -2  # exponent of 10, is the minimum value of lambda to try
    krls_max_lambda = -1  # exponent of 10, is the maximum value of lambda to try
    krls_n_gamma_to_try = 10  # number of gamma to try
    krls_min_gamma = -1.5 # exponent of 10, is the minimum value of gamma to try
    krls_max_gamma = -0.5  # exponent of 10, is the maximum value of gamma to try

    #read the dataset only the first time (I doesn't change)
    print('Reading dataset...')
    test = DataPreProccesingCat._read_file(test_filename)
    df = DataPreProccesingCat._read_file(input_filename)

    x_first = df.loc[:, df.columns != y_column]
    ytr = df[y_column]

    test_c = test.columns
    x_c = x_first.columns

    test_to_add = [x for x in x_c if x not in test_c]
    x_to_add = [x for x in test_c if x not in x_c]

    x_first = DataPreProccesingCat._add_columns(x_first, x_to_add)
    test = DataPreProccesingCat._add_columns(test, test_to_add)

    x_col = x_first.columns
    test = test.iloc[test.index][x_col]

    if not l2:
        val = x_first.values
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(val)
        xtr = pd.DataFrame(x_scaled)

        val_test = test.values
        min_max_scaler_test = preprocessing.MinMaxScaler()
        test_scaled = min_max_scaler_test.fit_transform(val_test)
        test = pd.DataFrame(test_scaled)
    else:
        test = normalize(test, axis=0)
        xtr = normalize(x_first, axis=0)

    if withLS:
        ls = Estimator.train_estimator(LinearRegression(), xtr, ytr, params={}, folds=folds)
        ls_result = ls.predict(test)
    if withRLS:
        rls_params = {'alpha': logspace(rls_min_lambda, rls_max_lambda, rls_n_lambda_to_try)}
        rls = Estimator.train_estimator(Ridge(solver='auto'), xtr, ytr, rls_params, folds=folds)
        rls_result = rls.predict(test)
    if withKRLS:
        print("Training KRLS...")
        krls_params = {
            'kernel': kernel_list,
            'alpha': logspace(krls_min_lambda, krls_max_lambda, krls_n_lambda_to_try),
            'gamma': logspace(krls_min_gamma, krls_max_gamma, krls_n_gamma_to_try)
        }
        krls = Estimator.train_estimator(KernelRidge(), xtr, ytr, krls_params, train_score=False, folds=folds)
        print(krls.best_params_, krls.best_score_)
        print("Predicting KRLS...")
        krls_result = krls.predict(test)
        print("Predicted")
        #DataFrame construction for Kaggle
        file_output = open("Output/output.csv", "w")
        file_output.write("Id,SalePrice\n")
        for res in range(len(krls_result)):
            file_output.write(str(1461+res)+","+str(krls_result[res])+"\n")
        file_output.close()
    print("HELLOOOO")

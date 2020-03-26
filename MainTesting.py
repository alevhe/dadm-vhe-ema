from sklearn import preprocessing
from numpy import logspace
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.preprocessing import normalize
import DatasetPreparation
import Estimator

if __name__ == '__main__':
    #initialize the params
    input_filename = 'data/train.csv'#name of the fail to be trained
    test_filename = 'data/test.csv'  # name of the fail to be trained
    y_column = 'SalePrice' #label of the results column
    withLS = False
    withRLS = False
    withKRLS = True
    folds = 3
    rls_n_lambda_to_try = 8  # number of lambda to try
    rls_min_lambda = -3  # exponent of 10, is the minimum value of lambda to try
    rls_max_lambda = 1  # exponent of 10, is the maximum value of lambda to try
    kernel_list = ['rbf', 'poly', 'laplacian']  # list of the kernel to be used
    krls_n_lambda_to_try = 15  # number of lambda to try
    krls_min_lambda = -1.52  # exponent of 10, is the minimum value of lambda to try
    krls_max_lambda = -1.48  # exponent of 10, is the maximum value of lambda to try
    krls_n_gamma_to_try = 15  # number of gamma to try
    krls_min_gamma = -0.62 # exponent of 10, is the minimum value of gamma to try
    krls_max_gamma = -0.58  # exponent of 10, is the maximum value of gamma to try

    #read the dataset only the first time (I doesn't change)
    print('Reading dataset...')
    test = DatasetPreparation._read_file(test_filename)

    df = DatasetPreparation._read_file(input_filename)

    x_first = df.loc[:, df.columns != y_column]
    ytr = df[y_column]

    test = normalize(test, axis=0)
    xtr = normalize(x_first, axis=0)
    """
    "Standard" Normalization
    
    val = x_first.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(val)
    xtr = pd.DataFrame(x_scaled)
    
    val_test = test.values
    min_max_scaler_test = preprocessing.MinMaxScaler()
    test_scaled = min_max_scaler_test.fit_transform(val_test)
    test = pd.DataFrame(test_scaled)
    """

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
        krls = Estimator.train_estimator(KernelRidge(), xtr, ytr, krls_params, folds=folds)
        print(krls.best_params_, krls.best_score_)
        print("Predicting KRLS...")
        krls_result = krls.predict(test)
        print("Predicted")
        #DataFrame construction for Kaggle
        file_output = open("Output/output-13210.csv", "w")
        file_output.write("Id,SalePrice\n")
        for res in range(len(krls_result)):
            file_output.write(str(1461+res)+","+str(krls_result[res])+"\n")
        file_output.close()
    print("HELLOOOO")

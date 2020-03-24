from sys import stderr
from numpy import logspace

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge

import DatasetPreparation
import ml
import PlotVisualization


def debug(*args):
    print('\033[35m', *args, '\033[m', file=stderr)


def main(params_no=2,  limit=100000, show_stats=True, ts_size=0.33, folds=3, montecarlo=100):
    ls_results = list()
    rls_results = list()
    krls_results = list()
    for routine in range(montecarlo):
        debug('%d - Reading dataset...' % routine)
        df = DatasetPreparation._read_file().iloc[:limit]

        debug('%d - Preparing dataset...' % routine)
        xtr, xts, ytr, yts = ml.prepare_dataset(df, 'SalePrice', ts_size=ts_size)

        rls_params = {'alpha': logspace(-4, 3, params_no)}
        krls_params = {
            'kernel': [
                'rbf',
                'poly',
                'laplacian'
            ],
            'alpha': logspace(-5, 1, params_no),
            'gamma': logspace(-5, 1, params_no)
        }

        debug('%d - Training LS...' % routine)
        ls = ml.train_estimator(LinearRegression(), xtr, ytr, folds=folds)
        debug('%d - Testing LS...' % routine)
        ls_score = ml.test_estimator(ls, xts, yts)
        for t in ls_score.index:
            temp = ls_score.iloc[t][ls_score.columns]
            ls_results.append(temp)

        debug('%d - Training RLS...' % routine)
        # solver='auto' diversi metodi per le routine computazionali in base al tipo di dato
        rls = ml.train_estimator(Ridge(solver='auto'), xtr, ytr, rls_params, folds=folds)
        debug('%d - Testing RLS...' % routine)
        rls_score = ml.test_estimator(rls, xts, yts)
        for t in rls_score.index:
            temp = rls_score.iloc[t][rls_score.columns]
            rls_results.append(temp)

        debug('%d - Training KRLS...' % routine)
        krls = ml.train_estimator(KernelRidge(), xtr, ytr, krls_params, folds=folds)
        debug('%d - Testing KRLS...' % routine)
        krls_score = ml.test_estimator(krls, xts, yts)
        for t in krls_score.index:
            temp = krls_score.iloc[t][krls_score.columns]
            krls_results.append(temp)

    file_1 = open("PlotData/" + "LS-" + str(ts_size) + "-" + str(folds) + ".txt", "a")
    for tt in ls_results:
        file_1.write(str(tt['mean_test_score']) + "," + str(tt['mean_train_score']) + ";")
    file_1.close()
    file_2 = open("PlotData/" + "RLS-" + str(ts_size) + "-" + str(folds) + ".txt", "a")
    for tt in rls_results:
        file_2.write(
            str(tt['param_alpha']) + "," + str(tt['mean_test_score']) + "," + str(tt['mean_train_score']) + ";")
    file_2.close()
    file_3 = open("PlotData/" + "KRLS-" + str(ts_size) + "-" + str(folds) + ".txt", "a")
    for tt in krls_results:
        file_3.write(tt['param_kernel'] + "," + str(tt['param_gamma']) + "," + str(tt['param_alpha']) + "," + str(
                tt['mean_test_score']) + "," + str(tt['mean_train_score']) + ";")
    file_3.close()

    print(" ")
    print("LS RESULTS :")
    # print(ls_score)
    print(ls_score.rename(columns={'mean_test_score': 'Mean Test Score', 'mean_train_score': 'Mean Train Score'}).iloc[
              ls_score['mean_test_score'].idxmax()])
    print(" ")

    print("RLS RESULTS :")
    # print(rls_score.iloc[rls_score['mean_test_score'].idxmax()])
    print(rls_score.rename(columns={'param_alpha': 'Alpha', 'mean_test_score': 'Mean Test Score',
                                    'mean_train_score': 'Mean Train Score'}).iloc[
              rls_score['mean_test_score'].idxmax()])
    print(" ")

    print("KRLS RESULTS :")
    # print(krls_score)
    # print(krls_score.iloc[krls_score['mean_test_score'].idxmax()])
    print(krls_score.rename(
        columns={'param_alpha': 'Alpha', 'mean_test_score': 'Mean Test Score', 'mean_train_score': 'Mean Train Score',
                 'param_kernel': 'Kernel', 'param_gamma': 'Gamma'}).iloc[krls_score['mean_test_score'].idxmax()])


if __name__ == '__main__':
    main(params_no=8, folds=2, limit=1000, montecarlo=1)
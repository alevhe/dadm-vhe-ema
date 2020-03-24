from sys import stderr
from numpy import logspace

import pandas as pd
import matplotlib.pylab as plt
from mpl_toolkits import mplot3d

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge

import dataset
import ml


def debug(*args):
    print('\033[35m', *args, '\033[m', file=stderr)


def main(params_no=2,  limit=100000, show_stats=True, ts_size=0.33, folds=3, montecarlo=100):
    ls_results = list()
    rls_results = list()
    krls_results = list()
    for routine in range(montecarlo):
        debug('%d - Reading dataset...' % routine)
        df = dataset.get_dataset().iloc[:limit]

        debug('%d - Preparing dataset...' % routine)
        xtr, xts, ytr, yts = ml.prepare_dataset(df, 'price', ts_size=ts_size)

        rls_params = {'alpha': logspace(-3, 1, params_no)}
        krls_params = {
            'kernel': [
                'rbf',
                'poly',
                'laplacian'
            ],
            'alpha': logspace(-3, 1, params_no),
            'gamma': logspace(-3, 1, params_no)
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

    lamb = list()
    ine = 0
    list_1 = list()
    list_2 = list()
    for tu in ls_results:
        lamb.append(ine)
        ine += 1
        list_1.append(tu['mean_test_score'])
        list_2.append(tu['mean_train_score'])
    plt.plot(lamb, list_1, color='b', linestyle='', marker=".", markersize="8")
    plt.plot(lamb, list_2, color='r', linestyle='', marker=".", markersize="8")
    plt.show()

    list_1 = list()
    list_2 = list()
    lamb = list()
    for tu in rls_results:
        lamb.append(tu['param_alpha'])
        list_1.append(tu['mean_test_score'])
        list_2.append(tu['mean_train_score'])
    plt.plot(lamb, list_1, color='b', linestyle='', marker=".", markersize="8")
    plt.plot(lamb, list_2, color='r', linestyle='', marker=".", markersize="8")
    plt.show()

    list_1 = list()
    list_2 = list()
    gamm = list()
    lamb = list()
    for tu in krls_results:
        gamm.append(tu['param_gamma'])
        lamb.append(tu['param_alpha'])
        list_1.append(tu['mean_test_score'])
        list_2.append(tu['mean_train_score'])
    for index in range(len(lamb)-1):
        if lamb[index+1] > lamb[index]:
            temp = lamb[index+1]
            lamb[index+1] = lamb[index]
            lamb[index] = temp

            temp = gamm[index + 1]
            gamm[index + 1] = gamm[index]
            gamm[index] = temp

            temp = list_1[index + 1]
            list_1[index + 1] = list_1[index]
            list_1[index] = temp

            temp = list_2[index + 1]
            list_2[index + 1] = list_2[index]
            list_2[index] = temp
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for index in range(len(lamb)-1):
        index_start = index
        while lamb[index+1] == lamb[index]:
            index += 1
        lamb_a = list()
        gamm_a = list()
        list_a = list()
        for ii in range(index_start, index):
            lamb_a.append(lamb[ii])
            gamm_a.append(gamm[ii])
            list_a.append(list_1[ii])
        for ii in range(len(lamb_a)-1):
            if gamm_a[ii+1] > gamm_a[ii]:
                temp = lamb_a[ii+1]
                lamb_a[ii+1] = lamb_a[ii]
                lamb_a[ii] = temp

                temp = gamm_a[ii + 1]
                gamm_a[ii + 1] = gamm_a[ii]
                gamm_a[ii] = temp

                temp = list_a[ii + 1]
                list_a[ii + 1] = list_a[ii]
                list_a[ii] = temp

        ax.plot3D(lamb_a, gamm_a, list_a, 'gray')

    plt.xlabel("l")
    plt.ylabel("g")
    plt.show()
    #plt.plot(gamm, list_1, color='b', linestyle='', marker=".", markersize="8")
    #plt.plot(gamm, list_2, color='r', linestyle='', marker=".", markersize="8")
    #plt.show()

    print("LS RESULTS :")
    print(ls_score)

    print("RLS RESULTS :")
    print(rls_score)

    print("KRLS RESULTS :")
    #print(krls_score)
    print(krls_score.iloc[krls_score['mean_test_score'].idxmax()])


if __name__ == '__main__':
    main(params_no=4, folds=2, limit=1000, montecarlo=1)
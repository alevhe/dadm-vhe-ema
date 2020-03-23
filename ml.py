import numpy as np
from time import time
import pandas as pd

from sklearn.model_selection import train_test_split, ParameterGrid, GridSearchCV, KFold
from sklearn.preprocessing import normalize


def prepare_dataset(df, y_col, ts_size=0.33):
    dfn = normalize(df, axis=0)
    dfn = pd.DataFrame(dfn, columns=df.columns)

    x = dfn.loc[:, dfn.columns != y_col]
    y = dfn[y_col]

    xtr, xts, ytr, yts = train_test_split(x, y, test_size=ts_size, shuffle=True)

    return xtr, xts, ytr, yts


def train_estimator(estimator, xtr, ytr, params={}, folds=2):
    cv = KFold(n_splits=folds)

    clf = GridSearchCV(estimator, params, cv=cv, iid=False, return_train_score=True, verbose=1, n_jobs=4)

    clf.fit(xtr, ytr)

    return clf


def test_estimator(estimator, xts, yts, show_stats=False, limit=10):
    if show_stats:
        print_stats(estimator, limit=limit)

    return estimator.score(xts, yts)


def print_stats(clf, limit=10):
    df = pd.DataFrame(clf.cv_results_)
    df = df.filter(regex='^mean.*score$|^std.*score$|^param_')

    df = df.sort_values('mean_test_score', ascending=False)

    print(df.iloc[:limit])


'''
for alpha in ...:
    r_i = Ridge(alpha)

br = best(r)    # coefficienti migliori di ridge

[RIPETI PER KERNEL] (KernelRidge)

bk = best(k)

bb = best(br, bk)    # modello e` non lineare?

bb(x, y) -> SCORE actual
'''

'''
PAIRWISE_KERNEL_FUNCTIONS = {
    'additive_chi2': additive_chi2_kernel,
    'chi2': chi2_kernel,
    'linear': linear_kernel,
    'polynomial': polynomial_kernel,
    'poly': polynomial_kernel,
    'rbf': rbf_kernel,
    'laplacian': laplacian_kernel,
    'sigmoid': sigmoid_kernel,
    'cosine': cosine_similarity, }
    

from sklearn.model_selection import ParameterGrid, GridSearchCV


xtr, ytr, xts, yts = ...

params = [
	{
		'kernel': ['linear']
	},
	{
		'kernel': ['rbf'],
		'gamma': [1, 10]
	}
]


##### TODO #####
test linear ^
    cv: piu` risultati per ciascun parametro, maggiore affidabilita`
    ottengo migliori parametri
    -- fold size?
        https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
        A model is trained using k-1 of the folds as training data
        https://scikit-learn.org/stable/modules/classes.html#splitter-classes
test non-linear ^
compare
pick best
final validation set --> results
'''
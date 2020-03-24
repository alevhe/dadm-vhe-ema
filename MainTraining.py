import getopt
import sys
from numpy import logspace

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.kernel_ridge import KernelRidge

import DatasetPreparation
import ml

if __name__ == '__main__':
    #initialize the params
    filename = 'data/train.csv'#name of the fail to be trained
    y_column = 'SalePrice' #label of the results column
    testing_size = 0.33 #percentage of testing set over total
    folds = 2 #folds-1 train and the other test for folds time to try different params
    max_dimension = 1000 #the dataset is a subset of the dataset stored in file
    montecarlo = 2 #number of repetitions for better accuracy
    rls_n_lambda_to_try = 8 #number of lambda to try
    rls_min_lambda = -3 #exponent of 10, is the minimum value of lambda to try
    rls_max_lambda = 1  #exponent of 10, is the maximum value of lambda to try
    kernel_list = ['rbf','poly','laplacian'] #list of the kernel to be used
    krls_n_lambda_to_try = 8 #number of lambda to try
    krls_min_lambda = -3 #exponent of 10, is the minimum value of lambda to try
    krls_max_lambda = 1  #exponent of 10, is the maximum value of lambda to try
    krls_n_gamma_to_try = 8 #number of gamma to try
    krls_min_gamma = -3 #exponent of 10, is the minimum value of gamma to try
    krls_max_gamma = 1  #exponent of 10, is the maximum value of gamma to try
    printResults = True #if to print results at the end
    saveResults = True #if to store data to the predefined file

    #check if there are params passed through command line
    help_string = "MainTraining.py\n " \
                  " -F <name of the file to be trained>\n " \
                  " -y <label of the results column>\n " \
                  " -s <percentage of testing set over total>\n " \
                  " -f <folds-1 train and the other test for folds time to try different params>\n " \
                  " -M <the dataset is a subset of the dataset stored in file>\n " \
                  " -r <number of repetitions for better accuracy>\n " \
                  " -p <1 if print results at the end, 0 otherwise>\n" \
                  " -S <1 if store data to the predefined file, 0 otherwise>\n" \
                  " -a <number of lambda to try in RLS>\n" \
                  " -b <number of lambda to try in KRLS>\n" \
                  " -c <number of gamma to try in KRLS>\n" \
                  " -d <exponent of 10, is the minimum value of lambda to try in RLS>\n" \
                  " -D <exponent of 10, is the minimum value of lambda to try in RLS>\n" \
                  " -g <exponent of 10, is the minimum value of lambda to try in KRLS>\n" \
                  " -g <exponent of 10, is the minimum value of lambda to try in KRLS>\n" \
                  " -h <exponent of 10, is the minimum value of gamma to try in KRLS>\n" \
                  " -H <exponent of 10, is the minimum value of gamma to try in KRLS>\n" \
                  " -k <kernel list, interleaved by a comma >"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hF:y:s:f:M:r:p:S:a:b:c:d:D:g:G:h:H:k:",
                                   ["file=", "label=", "testing=", "folds=", "maxDim=", "montecarlo=", "print=",
                                    "save=", "rlsL=", "krlsL=", "krlsG=", "rlsMinL=", "rlsMaxL=", "krlsMinL=",
                                    "krlsMaxL=", "krlsMinG=", "krlsMaxG=", "kernel="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-F", "--file"):
            filename = arg
        elif opt in ("-y", "--label"):
            y_column = arg
        elif opt in ("-s", "--testing"):
            testing_size = float(arg)
        elif opt in ("-f", "--folds"):
            folds = int(arg)
        elif opt in ("-M", "--maxDim"):
            max_dimension = int(arg)
        elif opt in ("-r", "--montecarlo"):
            montecarlo = int(arg)
        elif opt in ("-p", "--print"):
            if arg == "1":
                printResults = True
            elif arg == "0":
                printResults = False
            else:
                print(help_string)
                sys.exit(2)
        elif opt in ("-S", "--save"):
            if arg == "1":
                saveResults = True
            elif arg == "0":
                saveResults = False
            else:
                print(help_string)
                sys.exit(2)
        elif opt in ("-a", "--rlsL"):
            rls_n_lambda_to_try = int(arg)
        elif opt in ("-b", "--krlsL"):
            krls_n_lambda_to_try = int(arg)
        elif opt in ("-c", "--krlsG"):
            krls_n_gamma_to_try = int(arg)
        elif opt in ("-d", "--rlsMinL"):
            rls_min_lambda = int(arg)
        elif opt in ("-D", "--rlsMaxL"):
            rls_max_lambda = int(arg)
        elif opt in ("-g", "--krlsMinL"):
            krls_min_lambda = int(arg)
        elif opt in ("-G", "--krlsMaxL"):
            krls_max_lambda = int(arg)
        elif opt in ("-h", "--krlsMinG"):
            krls_min_gamma = int(arg)
        elif opt in ("-H", "--krlsMaxG"):
            krls_max_gamma= int(arg)
        elif opt in ("-k", "--kernel"):
            kernel_list = arg.split(",")

    #store the results of the different algorithms
    ls_results = list()
    rls_results = list()
    krls_results = list()

    #best result for all the algorithm
    best_ls = None
    best_rls = None
    best_krls = None

    #read the dataset only the first time (I doesn't change)
    print('Reading dataset...')
    df = DatasetPreparation._read_file(filename).iloc[:max_dimension]

    #for all the attempts
    for attempt in range(montecarlo):

        print('%d - Preparing dataset...' % attempt)
        #obtain 4 different matrix (x-train, x-test, y-train, y-test)
        xtr, xts, ytr, yts = ml.prepare_dataset(df, y_column, ts_size=testing_size)

        # LS algorithm
        print('%d - Training LS...' % attempt)
        ls = ml.train_estimator(LinearRegression(), xtr, ytr, folds=folds)
        print('%d - Testing LS...' % attempt)
        ls_score = ml.test_estimator(ls, xts, yts)
        if saveResults:
            for t in ls_score.index:
                #get the actual row and all the columns in the dataframe
                ls_results.append(ls_score.iloc[t][ls_score.columns])
        if printResults and (best_ls is None or ls_score.iloc[ls_score['mean_test_score'].idxmax()]['mean_test_score'] >
                             best_ls['Mean Test Score']):
                best_ls = ls_score.rename(columns={'mean_test_score': 'Mean Test Score', 'mean_train_score': 'Mean Train Score'}).iloc[ls_score['mean_test_score'].idxmax()]

        # RLS algorithm
        rls_params = {'alpha': logspace(rls_min_lambda, rls_max_lambda, rls_n_lambda_to_try)}
        print('%d - Training RLS...' % attempt)
        # solver='auto' different methods for the computational routines based on the data types
        rls = ml.train_estimator(Ridge(solver='auto'), xtr, ytr, rls_params, folds=folds)
        print('%d - Testing RLS...' % attempt)
        rls_score = ml.test_estimator(rls, xts, yts)
        if saveResults:
            for t in rls_score.index:
                #get the actual row and all the columns in the dataframe
                rls_results.append(rls_score.iloc[t][rls_score.columns])
        if printResults and (
                best_rls is None or rls_score.iloc[rls_score['mean_test_score'].idxmax()]['mean_test_score'] > best_rls[
            'Mean Test Score']):
            best_rls = rls_score.rename(columns={'param_alpha': 'Alpha', 'mean_test_score': 'Mean Test Score',
                                                 'mean_train_score': 'Mean Train Score'}).iloc[
                rls_score['mean_test_score'].idxmax()]

        # KRLS algorithm
        krls_params = {
            'kernel': kernel_list,
            'alpha': logspace(krls_min_lambda, krls_max_lambda, krls_n_lambda_to_try),
            'gamma': logspace(krls_min_gamma, krls_max_gamma, krls_n_gamma_to_try)
        }

        print('%d - Training KRLS...' % attempt)
        krls = ml.train_estimator(KernelRidge(), xtr, ytr, krls_params, folds=folds)
        print('%d - Testing KRLS...' % attempt)
        krls_score = ml.test_estimator(krls, xts, yts)
        if saveResults:
            for t in krls_score.index:
                #get the actual row and all the columns in the dataframe
                krls_results.append(krls_score.iloc[t][krls_score.columns])
        if printResults and (
                best_krls is None or krls_score.iloc[krls_score['mean_test_score'].idxmax()]['mean_test_score'] > best_krls[
            'Mean Test Score']):
            best_krls = krls_score.rename(
                columns={'param_alpha': 'Alpha', 'mean_test_score': 'Mean Test Score',
                         'mean_train_score': 'Mean Train Score',
                         'param_kernel': 'Kernel', 'param_gamma': 'Gamma'}).iloc[krls_score['mean_test_score'].idxmax()]

    if saveResults:
        if len(ls_results) != 0:
            file_1 = open("PlotData/" + "LS-" + str(testing_size) + "-" + str(folds) + ".txt", "a")
            for tt in ls_results:
                file_1.write(str(tt['mean_test_score']) + "," + str(tt['mean_train_score']) + ";")
            file_1.close()

        if len(rls_results) != 0:
            file_2 = open("PlotData/" + "RLS-" + str(testing_size) + "-" + str(folds) + ".txt", "a")
            for tt in rls_results:
                file_2.write(
                    str(tt['param_alpha']) + "," + str(tt['mean_test_score']) + "," + str(tt['mean_train_score']) + ";")
            file_2.close()
        if len(krls_results) != 0:
            file_3 = open("PlotData/" + "KRLS-" + str(testing_size) + "-" + str(folds) + ".txt", "a")
            for tt in krls_results:
                file_3.write(
                    tt['param_kernel'] + "," + str(tt['param_gamma']) + "," + str(tt['param_alpha']) + "," + str(
                        tt['mean_test_score']) + "," + str(tt['mean_train_score']) + ";")
            file_3.close()

    if printResults:
        if best_ls is not None:
            print("")
            print("LS RESULTS :")
            print(best_ls)
        if best_rls is not None:
            print("")
            print("RLS RESULTS :")
            print(best_rls)
        if best_krls is not None:
            print("")
            print("KRLS RESULTS :")
            print(best_krls)

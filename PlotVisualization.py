import matplotlib.pylab as plt

def plot(ls_results, rls_results, krls_results):
    lamb = list()
    ine = 0
    list_1 = list()
    list_2 = list()
    for tu in ls_results:
        lamb.append(ine)
        ine += 1
        list_1.append(tu['mean_test_score'])
        list_2.append(tu['mean_train_score'])
    plt.plot(lamb, list_1, color='b', linestyle='-', marker=".", markersize="8")
    plt.plot(lamb, list_2, color='r', linestyle='-', marker=".", markersize="8")
    plt.show()

    list_1 = list()
    list_2 = list()
    lamb = list()
    for tu in rls_results:
        lamb.append(tu['param_alpha'])
        list_1.append(tu['mean_test_score'])
        list_2.append(tu['mean_train_score'])
    plt.plot(lamb, list_1, color='b', linestyle='-', marker=".", markersize="8")
    plt.plot(lamb, list_2, color='r', linestyle='-', marker=".", markersize="8")
    plt.xscale("log")
    plt.show()

    list_1 = list()
    list_2 = list()
    gamm = list()
    lamb = list()
    for tu in krls_results:
        gamm.append(tu['param_gamma'])
        lamb.append(tu['param_alpha'])
        if tu['mean_test_score'] > 0.7:
            list_1.append(tu['mean_test_score'])
        else:
            list_1.append(0.7)
        if tu['mean_train_score'] > 0.7:
            list_2.append(tu['mean_train_score'])
        else:
            list_2.append(0.7)
    cmap = plt.plasma()
    f, ax = plt.subplots()
    ax.set_title("Mean Test Score")
    ax.set_ylabel('gamma')
    ax.set_xlabel('lambda')
    points = ax.scatter(gamm, lamb, c=list_1, s=50, cmap=cmap)
    f.colorbar(points)
    plt.yscale("log")
    plt.xscale("log")
    plt.show()
    f, ax = plt.subplots()
    ax.set_title("Mean Train Score")
    ax.set_ylabel('gamma')
    ax.set_xlabel('lambda')
    points = ax.scatter(gamm, lamb, c=list_2, s=50, cmap=cmap)
    f.colorbar(points)
    plt.yscale("log")
    plt.xscale("log")
    plt.show()
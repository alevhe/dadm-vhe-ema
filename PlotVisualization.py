import matplotlib.pylab as plt

def swap(list, id1, id2):
    temp = list[id1]
    list[id1] = list[id2]
    list[id2] = temp

if __name__ == '__main__':
    folder = "PlotData"
    ls_input = "LS-0.33-2.txt"
    rls_input = "RLS-0.33-2.txt"
    krls_input = "KRLS-0.33-2.txt"
    limit_value = 0.7

    file_read = open(folder + "/" + ls_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    x = list()
    index = 0
    train_score = list()
    test_score = list()
    for row in input_data:
        if row == '':
            continue
        tu = row.split(",")
        x.append(index)
        index += 1
        test_score.append(float(tu[0]))
        train_score.append(float(tu[1]))
    plt.plot(x, train_score, color='b', linestyle='-', marker=".", markersize=5, label="train score")
    plt.plot(x, test_score, color='r', linestyle='-', marker=".", markersize=5, label="test score")
    plt.xlabel("Iterazioni")
    plt.ylabel("Mean score")
    plt.title("LS results")
    plt.legend(frameon=False, loc='lower center')
    plt.show()

    file_read = open(folder + "/" + rls_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    alpha = list()
    train_score = list()
    test_score = list()
    for row in input_data:
        if row == '':
            continue
        tu = row.split(",")
        alpha.append(float(tu[0]))
        test_score.append(float(tu[1]))
        train_score.append(float(tu[2]))
    for id1 in range(len(alpha)-1):
        for id2 in range(id1+1, len(alpha)):
            if alpha[id2] < alpha[id1]:
                swap(alpha, id1, id2)
                swap(train_score, id1, id2)
                swap(test_score, id1, id2)
    train = list()
    test = list()
    x = list()
    index = -1
    while index < len(alpha)-1:
        index += 1
        start_index = index
        while index < len(alpha)-1 and alpha[index] == alpha[index+1]:
            index += 1
        sum_train = 0
        sum_test = 0
        for id1 in range(start_index, index+1):
            sum_train += train_score[id1]
            sum_test += test_score[id1]
        train.append(sum_train/(index-start_index+1))
        test.append(sum_test/(index-start_index+1))
        x.append(alpha[index])
    plt.plot(x, train, color='b', linestyle='-', marker=".", markersize=5, label="train score")
    plt.plot(x, test, color='r', linestyle='-', marker=".", markersize=5, label="test score")
    plt.xlabel("lambda")
    plt.ylabel("Mean score")
    plt.title("RLS results")
    plt.legend(frameon=False, loc='lower center')
    plt.xscale("log")
    plt.show()

    file_read = open(folder + "/" + krls_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    alpha_orig = list()
    gamma_orig = list()
    kernel_orig = list()
    train_score_orig = list()
    test_score_orig = list()
    for row in input_data:
        if row == '':
            continue
        tu = row.split(",")
        kernel_orig.append(tu[0])
        gamma_orig.append(float(tu[1]))
        alpha_orig.append(float(tu[2]))
        test_score_orig.append(float(tu[3]))
        train_score_orig.append(float(tu[4]))

    kernel_list = list()
    for ker in kernel_orig:
        if ker not in kernel_list:
            kernel_list.append(ker)

    for kernel in kernel_list:
        alpha = list()
        gamma = list()
        train_score = list()
        test_score = list()
        for value in range(len(kernel_orig)):
            if kernel_orig[value] == kernel:
                alpha.append(alpha_orig[value])
                gamma.append(gamma_orig[value])
                train_score.append(train_score_orig[value])
                test_score.append(test_score_orig[value])
        for id1 in range(len(alpha) - 1):
            for id2 in range(id1 + 1, len(alpha)):
                if alpha[id2] < alpha[id1]:
                    swap(alpha, id1, id2)
                    swap(gamma, id1, id2)
                    swap(train_score, id1, id2)
                    swap(test_score, id1, id2)
        index = -1
        while index < len(alpha) - 1:
            index += 1
            start_index = index
            while index < len(alpha) - 1 and alpha[index] == alpha[index + 1]:
                index += 1
            for id1 in range(start_index, index):
                for id2 in range(id1 + 1, index + 1):
                    if gamma[id2] < gamma[id1]:
                        swap(alpha, id1, id2)
                        swap(gamma, id1, id2)
                        swap(train_score, id1, id2)
                        swap(test_score, id1, id2)
        train = list()
        test = list()
        x = list()
        y = list()
        index = -1
        while index < len(alpha) - 1:
            index += 1
            start_index = index
            while index < len(alpha) - 1 and alpha[index] == alpha[index + 1] and gamma[index] == gamma[index + 1]:
                index += 1
            sum_train = 0
            sum_test = 0
            for id1 in range(start_index, index + 1):
                sum_train += train_score[id1]
                sum_test += test_score[id1]
            train_value = sum_train / (index - start_index + 1)
            test_value = sum_test / (index - start_index + 1)
            if train_value > limit_value:
                train.append(train_value)
            else:
                train.append(limit_value)
            if test_value > limit_value:
                test.append(test_value)
            else:
                test.append(limit_value)
            x.append(alpha[index])
            y.append(gamma[index])
        cmap = plt.plasma()
        f, ax = plt.subplots()
        ax.set_title("KRLS results - "+kernel+" - Mean Test Score")
        ax.set_ylabel('gamma')
        ax.set_xlabel('lambda')
        points = ax.scatter(x, y, c=test, s=50, cmap=cmap)
        f.colorbar(points)
        plt.yscale("log")
        plt.xscale("log")
        plt.show()
        f, ax = plt.subplots()
        ax.set_title("KRLS results - "+kernel+" - Mean Train Score")
        ax.set_ylabel('gamma')
        ax.set_xlabel('lambda')
        points = ax.scatter(x, y, c=train, s=50, cmap=cmap)
        f.colorbar(points)
        plt.yscale("log")
        plt.xscale("log")
        plt.show()

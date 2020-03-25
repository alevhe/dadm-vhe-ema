import matplotlib.pylab as plt

def swap(list, id1, id2):
    temp = list[id1]
    list[id1] = list[id2]
    list[id2] = temp

if __name__ == '__main__':

    # Variable of the execution
    PlotFolder = "TestData"
    ls_input = "LS-0.33-2.txt"
    rls_input = "RLS-0.33-2.txt"
    krls_input = "KRLS-0.33-2.txt"

    #lower bound for the score when analyzing krls (because of the color scale)
    limit_value_for_krls = 0.7

    #limits for lambda (they allow to zoom areas)
    rls_min_lambda = 0.0001
    rls_max_lambda = 1000

    #limits for gamma (they allow to zoom areas)
    krls_min_lambda = 0.0001
    krls_max_lambda = 1000
    krls_min_gamma = 0.0001
    krls_max_gamma = 1000

    #color map for the kernel plots
    cmap = plt.plasma()

    # LS algorithm
    #open the selected file and read splitting on ;
    file_read = open(PlotFolder + "/" + ls_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    x = list()
    index = 0
    score = list()
    for row in input_data:
        #the last char in the file is ;
        if row == '':
            continue
        x.append(index)
        index += 1
        score.append(float(row))
    plt.plot(x, score, color='r', linestyle='-', marker=".", markersize=5, label="test score")
    plt.xlabel("Iterazioni")
    plt.ylabel("Mean score")
    plt.title("LS results")
    plt.legend(frameon=False, loc='lower center')
    plt.show()


    # RLS algorithm
    #open the selected file and read splitting on ;
    file_read = open(PlotFolder + "/" + rls_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    alpha = list()
    score = list()
    for row in input_data:
        #the last char in the file is ;
        if row == '':
            continue
        tu = row.split(",")
        a = float(tu[1])
        #select only the desired values of lambda
        if rls_min_lambda <= a and rls_max_lambda >= a:
            alpha.append(a)
            score.append(float(tu[0]))
    #sort all the vectors by lambda (alpha)
    for id1 in range(len(alpha)-1):
        for id2 in range(id1+1, len(alpha)):
            if alpha[id2] < alpha[id1]:
                swap(alpha, id1, id2)
                swap(score, id1, id2)
    test = list()
    x = list()
    index = -1
    while index < len(alpha)-1:
        index += 1
        start_index = index
        while index < len(alpha)-1 and alpha[index] == alpha[index+1]:
            index += 1
        sum_test = 0
        #between start_index and index (both included) the values have same lambda => take the average
        for id1 in range(start_index, index+1):
            sum_test += score[id1]
        test.append(sum_test/(index-start_index+1))
        x.append(alpha[index])
    plt.plot(x, test, color='r', linestyle='-', marker=".", markersize=5, label="test score")
    plt.xlabel("lambda")
    plt.ylabel("Mean score")
    plt.title("RLS results")
    plt.legend(frameon=False, loc='lower center')
    plt.xscale("log")
    plt.show()

    # KRLS algorithm
    # open the selected file and read splitting on ;
    file_read = open(PlotFolder + "/" + krls_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    alpha_orig = list()
    gamma_orig = list()
    kernel_orig = list()
    score_orig = list()
    for row in input_data:
        #the last char in the file is ;
        if row == '':
            continue
        tu = row.split(",")
        a = float(tu[1])
        g = float(tu[2])
        # select only the desired values of lambda and gamma
        if krls_min_lambda <= a and krls_max_lambda >= a and krls_min_gamma <= g and krls_max_gamma >= g:
            gamma_orig.append(g)
            alpha_orig.append(a)
            kernel_orig.append(tu[3])
            score_orig.append(float(tu[0]))
    #create the kernel list
    kernel_list = list()
    for ker in kernel_orig:
        if ker not in kernel_list:
            kernel_list.append(ker)
    #analyze one by one all the kernels
    for kernel in kernel_list:
        alpha = list()
        gamma = list()
        test_score = list()
        #look through all the data read by file and select those which have this kernel
        for value in range(len(kernel_orig)):
            if kernel_orig[value] == kernel:
                alpha.append(alpha_orig[value])
                gamma.append(gamma_orig[value])
                test_score.append(score_orig[value])
        #sort all the data whit this kernel by lambda
        for id1 in range(len(alpha) - 1):
            for id2 in range(id1 + 1, len(alpha)):
                if alpha[id2] < alpha[id1]:
                    swap(alpha, id1, id2)
                    swap(gamma, id1, id2)
                    swap(test_score, id1, id2)
        index = -1
        while index < len(alpha) - 1:
            index += 1
            start_index = index
            #all the elements between start_index and index (both inclusive) have the same labda
            while index < len(alpha) - 1 and alpha[index] == alpha[index + 1]:
                index += 1
            #sort those elements by gamma
            for id1 in range(start_index, index):
                for id2 in range(id1 + 1, index + 1):
                    if gamma[id2] < gamma[id1]:
                        swap(alpha, id1, id2)
                        swap(gamma, id1, id2)
                        swap(test_score, id1, id2)
        test = list()
        x = list()
        y = list()
        index = -1
        while index < len(alpha) - 1:
            index += 1
            start_index = index
            #all the elemnts between start_index and index have the same lambda and gamma
            while index < len(alpha) - 1 and alpha[index] == alpha[index + 1] and gamma[index] == gamma[index + 1]:
                index += 1
            sum_test = 0
            #take the average of those elements
            for id1 in range(start_index, index + 1):
                sum_test += test_score[id1]
            test_value = sum_test / (index - start_index + 1)
            #use only the values grater than limit_value_for_krls. In this way you can change the color scale
            if test_value > limit_value_for_krls:
                test.append(test_value)
            else:
                #if the value is lower, use the lower that you can use
                test.append(limit_value_for_krls)
            x.append(alpha[index])
            y.append(gamma[index])


#        plt.subplot(1, 1, 1)
        plt.title(kernel+" - Test")
        plt.ylabel('gamma')
        plt.xlabel('lambda')
        points = plt.scatter(x, y, c=test, s=10, cmap=cmap)
        plt.colorbar(points)
        plt.yscale("log")
        plt.xscale("log")
        plt.show()

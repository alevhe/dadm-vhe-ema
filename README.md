# Dataset
https://www.kaggle.com/harlfoxem/housesalesprediction

# Abstract
We applied three machine learning algorithms and compared the results.

The algorithms used are:
*  Least Squares
*  Regularized Least Squares
*  Kernel Regularized Least Squares
   *  RBF kernel
   *  Polynomial kernel
   *  Laplacian kernel

# Description
The dataset has been split in two sets:
*  Training
*  Testing

## Training
We performed k-fold cross validation for each algorithm on the training set.

K-fold cross validation splits the dataset into k groups.
One is used as validation set, the others *(k-1)* as training set.
The process is then repeated with a different fold combination.

The results are finally averaged across all folds.
In this way it is possible to obtain more accurate estimation of the best
parameters, since we reduce the risk of overfitting the training data.

## Testing
After having selected the best parameters for each algorithm, we try to predict
a new portion of the dataset, to get an idea of the actual accuracy of each
predictor.

# Results
We noticed the KRLS is the most accurate predictor, even though it takes the
longest time to train.

RLS provides a good tradeoff between training times and accuracy.

There is a consistent degree of difference between the accuracy obtained with
KRLS and RLS.
This means that the model presents some non-linearity.

LS, on the other hand, presents some interesting properties.
It is usually as accurate as RLS and takes less time to train.
However, it is very sensible to the training data: in some cases it happens to
be slighly more accurate than RLS, while sometimes it is extremely inaccurate.
This means that the model presents some linearity, but not in all samples.
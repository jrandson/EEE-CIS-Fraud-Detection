This repository was created to store the code for the Kaggle competition that aims to predict the probability that an online transaction is fraudulent, as denoted by the binary target isFraud. The data is broken into two files identity and transaction, which are joined by TransactionID. Not all transactions have corresponding identity information.

Check the notebook data-prep to see how the dataset was pre-porceeed before the train step
After that, to attempts was made to train the model, that differs in itself in way I have deald with the unbalanced data.

For this competition, It was choosed the xgboost algorithm dueto its flexiblidity and ensemble power.
More about it here: https://xgboost.readthedocs.io/en/latest/

More details,as well as, discutions about thhis comptetion can be found here: https://www.kaggle.com/c/ieee-fraud-detection/data


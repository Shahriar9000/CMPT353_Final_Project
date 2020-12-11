import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

def speedRegressor():



    return model

def actionClassifier():

    model = make_pipeline(
        # StandardScaler(),
        # KNeighborsClassifier(3) # 0.8875 0.825
        SVC(kernel='poly', degree=3, C=1) # 0.975 0.825
    )

    return model

def main():

    # # Action Classifier
    data = pd.read_csv('ml_input_data.csv')
    X = data.loc[:, data.columns != 'action']
    X = X.loc[:, X.columns != 'speed']
    y = data['action']

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, stratify = y) # , random_state = 0, stratify = y

    model = make_pipeline(
        # StandardScaler(),
        KNeighborsClassifier(4) # 0.8875 0.825
        # SVC(kernel='poly', degree=3, C=1) # 0.975 0.825
    )

    model.fit(X_train, y_train)
    print(model.score(X_train, y_train))
    print(model.score(X_valid, y_valid))

    # Speed Regressor
    # data = pd.read_csv('ml_input_data.csv')
    # data = data.loc[data.filter((data.action != 'upstairs'))]
    # print(data)
    # data = data.filter((data.action != 'downstairs'))
    # X = data.loc[:, data.columns != 'action']
    # X = X.loc[:, X.columns != 'speed']
    # y = data['speed']
    #
    # X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, stratify = y) # , random_state = 0, stratify = y
    #
    # model = make_pipeline(
    #     # StandardScaler(),
    #     KNeighborsClassifier(4) # 0.8875 0.825
    #     # SVC(kernel='poly', degree=3, C=1) # 0.975 0.825
    # )
    #
    # model.fit(X_train, y_train)
    # print(model.score(X_train, y_train))
    # print(model.score(X_valid, y_valid))

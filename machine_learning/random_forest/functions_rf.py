import pandas as pd
import os
import numpy as np
from machine_learning.random_forest.features import extractFeatures_Stock
from machine_learning.random_forest.features import extractFeatures_MA_Karle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from configurations.config import Config
from machine_learning.preparedata import prepareData
import matplotlib.pyplot as plt


def runRandomForest(data_raw, n_estimators, window_sizes , feature_type):
    results = {}
    grid = np.zeros((len(n_estimators), len(window_sizes)))
    num_combinations = len(n_estimators) * len(window_sizes)

    if isinstance(data_raw, str):
        data = pd.read_parquet(data_raw)
    else:
        data = data_raw

    print('---- Start GridSearch: ----')
    print('Rohdatei: ' + data_raw)
    print('Random Forest -- Infos:')
    print('\tFeatures: ' + feature_type)

    n = 1

    for i, n_estimator in enumerate(n_estimators):
        for j, window_size in enumerate(window_sizes):
            print('_________________________________________________________________')
            print(f'\tAnzahl Durchläufe: ' + str(n) + ' / ' + str(num_combinations))
            print(f'\tSample Length: {window_size}, N_Estimator: {n_estimator}')
            n += 1
            # Extraktion der Features:
            if feature_type == 'MA_Karle':
                features, labels = extractFeatures_MA_Karle(dataframe = data, window_size=window_size)
            elif feature_type == 'Standard':
                features, labels = extractFeatures_Stock(dataframe = data, window_size=window_size)

            ###############################################
            #Start Random Forest:
            ###############################################
            X = features
            y = labels

            # Splitting the dataset into training and testing sets (80% train, 20% test)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

            # Creating and training the Random Forest Classifier
            rf = RandomForestClassifier(n_estimators=n_estimator, random_state=42)
            rf.fit(X_train, y_train)

            # Predicting on the test set
            y_pred = rf.predict(X_test)

            # Genauigkeit berechnen
            accuracy = accuracy_score(y_test, y_pred)

            results[(n_estimator, window_size)] = accuracy
            grid[i, j] = accuracy

            print(f"\tAccuracy: {accuracy}")
            print('_________________________________________________________________')

    # Ausgabe gridsearch
    plt.figure(figsize=(8, 6))
    plt.imshow(grid, cmap='Blues', interpolation='nearest')

    for i in range(len(n_estimators)):
        for j in range(len(window_sizes)):
            plt.text(j, i, f'{grid[i, j] * 100:.2f}%', ha='center', va='center', color='black')

    plt.colorbar(label='Test Accuracy')
    plt.xticks(np.arange(len(window_sizes)), window_sizes)
    plt.yticks(np.arange(len(n_estimators)), n_estimators)
    plt.xlabel('Sample Length')
    plt.ylabel('N_Estimators')
    plt.title('Grid Search Results - Test Accuracy')
    plt.savefig(os.path.join(Config.PATH_data_machine_learning, 'grid_search_RF.png'))
    print('---- Ende GridSearch. ----')








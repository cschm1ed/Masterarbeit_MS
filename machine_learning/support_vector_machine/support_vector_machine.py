import pandas as pd
import os
from machine_learning.random_forest.features import extractFeatures_Stock
from configurations.config import Config
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def runSupportVectorMachine(data_raw, scaler_type):
    window_sizes = [18600, 9300, 3100, 1860, 100]
    kernels = ['rbf', 'linear', 'sigmoid']
    accuracy_results = []

    if isinstance(data_raw, str):
        data = pd.read_parquet(data_raw)
    else:
        data = data_raw


    for kernel in kernels:
        print('---- Start: ----')
        print('SupportVectorMachine -- Infos:')
        print('\tScaler: ' + scaler_type)
        print('\tKernel: ' + kernel)
        print('\tWindow Sizes: ' + str(window_sizes))

        for window_size in window_sizes:

            # Extraktion der Features:
            features, labels = extractFeatures_Stock(data, window_size=window_size)

            ###############################################
            # Start Support Vector Machine:
            ###############################################
            X = features
            Y = labels

            # Splitting the dataset into training and testing sets (80% train, 20% test)
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            # Train SVM
            svm = SVC(kernel=kernel, gamma='scale')
            svm.fit(X_train, y_train)


            # Predicting on the test set
            y_pred = svm.predict(X_test)

            # Ausgabe:
            print('----------------')
            print('Window Size: ' + str(window_size))
            print('Kernel: ' + kernel)
            # Genauigkeit berechnen
            accuracy = accuracy_score(y_test, y_pred)
            print(f'Genauigkeit: {accuracy:.5f}')
            print('----------------')

            # Liste zur Speicherung:
            accuracy_results.append({'Kernel': kernel, 'Window Size': window_size, 'Accuracy': accuracy})
        print('---- End: ' + kernel + '----')
    accuracy_df = pd.DataFrame(accuracy_results)
    print(accuracy_df)
    # Speichern des gesamten Dataframes in einer neuen .csv Datei:
    dateiname = 'SVM__results_' + scaler_type + '.txt'
    output_pfad = os.path.join(Config.PATH_data_machine_learning, dateiname)
    accuracy_df.to_csv(output_pfad, sep='\t', index=False)

    print('---- Ende. ----\n')
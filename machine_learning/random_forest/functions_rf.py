import pandas as pd
import os
from machine_learning.random_forest.features import extractFeatures
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from configurations.config import Config
from machine_learning.preparedata import prepareData


def runRandomForest(data_raw, n_estimators, scaler_type):
    window_sizes = [18600, 9300, 3100, 1860, 100, 10]
    accuracy_results = []
    if isinstance(data_raw, str):
        data = pd.read_parquet(data_raw)
    else:
        data = data_raw
    print('---- Start: ----')
    print('Random Forest -- Infos:')
    print('\tScaler: '+ scaler_type)
    print('\tn_estimators: ' + str(n_estimators))
    print('\tWindow Sizes: ' + str(window_sizes))

    for window_size in window_sizes:

        # Extraktion der Features:
        features, labels = extractFeatures(data, window_size=window_size)

        ###############################################
        #Start Random Forest:
        ###############################################
        X = features
        Y = labels

        # Splitting the dataset into training and testing sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Creating and training the Random Forest Classifier
        rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        rf.fit(X_train, y_train)

        # Predicting on the test set
        y_pred = rf.predict(X_test)

        # Ausgabe:
        print('----------------')
        print('Window Size: ' + str(window_size))
        # Genauigkeit berechnen
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Genauigkeit: {accuracy:.5f}')
        print('----------------')

        # Liste zur Speicherung:
        accuracy_results.append({'Window Size': window_size, 'Accuracy': accuracy})

    accuracy_df = pd.DataFrame(accuracy_results)
    print(accuracy_df)
    # Speichern des gesamten Dataframes in einer neuen .csv Datei:
    dateiname = 'RF_'+ str(n_estimators) + '_results_' + scaler_type + '.txt'
    output_pfad = os.path.join(Config.PATH_data_machine_learning, dateiname)
    accuracy_df.to_csv(output_pfad, sep='\t', index=False)

    print('---- Ende. ----\n')




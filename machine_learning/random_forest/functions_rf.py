import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from configurations.config import Config
import matplotlib.pyplot as plt
from joblib import dump
from scipy.signal import find_peaks
from scipy.fft import fft
import glob
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from joblib import load
import seaborn as sns

# ----
# FUNKTIONEN FÜR RANDOM FOREST MODELLE
# ----


# Funktion zum Features (Stock) extrahieren:
def extractFeatures_Stock(dataframe, sample_length):
    # Number of windows
    num_windows = len(dataframe) // sample_length

    # Initializing lists to store the extracted features and labels for each window
    features = []
    labels = []

    for i in range(num_windows):
        # Extracting a window from the dataset
        window = dataframe.iloc[i * sample_length:(i + 1) * sample_length]

        # Calculating features
        avg_current = np.mean(window['current_[mA]'])
        max_current = np.max(window['current_[mA]'])
        min_current = np.min(window['current_[mA]'])
        std_current = np.std(window['current_[mA]'])

        avg_position = np.mean(window['position_[mm]'])
        max_position = np.max(window['position_[mm]'])
        min_position = np.min(window['position_[mm]'])
        std_position = np.std(window['position_[mm]'])

        # Determining the most frequent label in the window
        label = window['label'].mode()[0]

        # Appending the features and label to the lists
        features.append(
            [avg_current, max_current, min_current, std_current, avg_position, max_position, min_position,
             std_position])
        labels.append(label)

    return pd.DataFrame(features,
                        columns=['Avg_Current', 'Max_Current', 'Min_Current', 'Std_Current', 'Avg_Position',
                                 'Max_Position', 'Min_Position', 'Std_Position']), labels


# Funktion zum Features (aus MA Karle) extrahieren:
def extractFeatures_MA_Karle(dataframe, sample_length):
    # Number of windows
    num_windows = len(dataframe) // sample_length

    # Initializing lists to store the extracted features and labels for each window
    features = []
    labels = []

    for i in range(num_windows):
        # Extracting a window from the dataset
        window = dataframe.iloc[i * sample_length:(i + 1) * sample_length]

        # Umwandlung der Datenreihe in ein NumPy-Array für einfache Berechnungen
        data_current = np.array(window['current_[mA]'])
        data_position = np.array(window['position_[mm]'])

        # Calculating features
        # 1. Minimale Differenz zwischen zwei Datenpunkten (Min diff)
        min_diff_current = np.min(np.abs(np.diff(data_current)))
        min_diff_position = np.min(np.abs(np.diff(data_position)))

        # 2. Belegte Bandbreite (obw99%)
        sorted_data = np.sort(data_current)
        obw99_index = int(len(sorted_data) * 0.99)
        obw99_current = sorted_data[obw99_index] - sorted_data[0]
        sorted_data = np.sort(data_position)
        obw99_index = int(len(sorted_data) * 0.99)
        obw99_position = sorted_data[obw99_index] - sorted_data[0]

        # 3. Summe aller Beträge der Differenzen zweier Datenpunkte (Sum diff abs)
        sum_diff_abs_current = np.sum(np.abs(np.diff(data_current)))
        sum_diff_abs_position = np.sum(np.abs(np.diff(data_position)))

        # 4. Wertebereich (Range)
        data_range_current = np.max(data_current) - np.min(data_current)
        data_range_position = np.max(data_position) - np.min(data_position)

        # 5. Minimum der 2. Ableitung (Min grad2)
        min_grad2_current = np.min(np.diff(data_current, n=2))
        min_grad2_position = np.min(np.diff(data_position, n=2))

        # 6. Anzahl der Maxima der Ableitung (N max grad)
        grad = np.diff(data_current)
        peaks, _ = find_peaks(grad)
        n_max_grad_current = len(peaks)
        grad = np.diff(data_position)
        peaks, _ = find_peaks(grad)
        n_max_grad_position = len(peaks)

        # 7. Gemittelte Frequenz (Mean frequence)
        frequencies = np.abs(fft(data_current))
        mean_frequence_current = np.mean(frequencies)
        frequencies = np.abs(fft(data_position))
        mean_frequence_position = np.mean(frequencies)

        # 8. Stärke der Asymmetrie (Skewness)
        # data_skewness_current = skew(data_current)
        # data_skewness_position = skew(data_position)

        # 9. Maximum (Max)
        max_value_current = np.max(data_current)
        max_value_position = np.max(data_position)

        # 10. Maximum der 2. Ableitung (Max grad2)
        max_grad2_current = np.max(np.diff(data_current, n=2))
        max_grad2_position = np.max(np.diff(data_position, n=2))

        # Determining the most frequent label in the window
        label = window['label'].mode()[0]

        # Appending the features and label to the lists
        features.append(
            [min_diff_current, obw99_current, sum_diff_abs_current, data_range_current, min_grad2_current,
             n_max_grad_current, mean_frequence_current, max_value_current, max_grad2_current,
             min_diff_position, obw99_position, sum_diff_abs_position, data_range_position, min_grad2_position,
             n_max_grad_position, mean_frequence_position, max_value_position,
             max_grad2_position])
        labels.append(label)

    # Creating a DataFrame with the features
    feature_columns = ['Min_Diff_Current', 'OBW99_Current', 'Sum_Diff_Abs_Current', 'Range_Current',
                       'Min_Grad2_Current', 'N_Max_Grad_Current', 'Mean_Frequence_Current',
                       'Max_Value_Current', 'Max_Grad2_Current', 'Min_Diff_Position', 'OBW99_Position',
                       'Sum_Diff_Abs_Position', 'Range_Position', 'Min_Grad2_Position', 'N_Max_Grad_Position',
                       'Mean_Frequence_Position', 'Max_Value_Position', 'Max_Grad2_Position']
    return pd.DataFrame(features, columns=feature_columns), labels


# Hauptskript zum RF Training mit GridSearch:
def trainRF_GridSearch(data_raw, n_estimators, sample_lengths, feature_type, scaler, output_dir):
    results = {}
    grid = np.zeros((len(n_estimators), len(sample_lengths)))
    num_combinations = len(n_estimators) * len(sample_lengths)

    if isinstance(data_raw, str):
        data = pd.read_parquet(data_raw)
    else:
        data = data_raw

    # Erstellen eines neuen Ordners als Speicherort der Ergebnisse
    ordnername = 'RF_' + scaler + 'Scaler'
    output_dir_2 = os.path.join(output_dir, ordnername)
    os.makedirs(output_dir_2)

    n = 1
    for i, n_estimator in enumerate(n_estimators):
        for j, sample_length in enumerate(sample_lengths):
            print('_________________________________________________________________')
            print(f'\tAnzahl Durchläufe: ' + str(n) + ' / ' + str(num_combinations))
            print(f'\tSample Length: {sample_length}, N_Estimator: {n_estimator}')
            n += 1
            # Extraktion der Features:
            if feature_type == 'MA_Karle':
                features, labels = extractFeatures_MA_Karle(dataframe=data, sample_length=sample_length)
            elif feature_type == 'Standard':
                features, labels = extractFeatures_Stock(dataframe=data, sample_length=sample_length)

            ###############################################
            # Start Random Forest:
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
            accuracy_short = round(accuracy, 4)

            results[(n_estimator, sample_length)] = accuracy
            grid[i, j] = accuracy

            # Speichern des Modells:
            model_filename = f'rf_{n_estimator}_{sample_length}_{accuracy_short}.joblib'
            model_path = os.path.join(output_dir_2, model_filename)
            dump(rf, model_path)

            print(f"\tAccuracy: {accuracy}")
            print('_________________________________________________________________')

    # Ausgabe gridsearch
    plt.figure(figsize=(7, 3))
    plt.imshow(grid, cmap='Blues', interpolation='nearest')

    for i in range(len(n_estimators)):
        for j in range(len(sample_lengths)):
            plt.text(j, i, f'{grid[i, j] * 100:.2f}%', ha='center', va='center', color='black')

    # plt.colorbar(label='Test Accuracy')
    plt.colorbar(label='Test Accuracy')
    plt.xticks(np.arange(len(sample_lengths)), sample_lengths)
    plt.yticks(np.arange(len(n_estimators)), n_estimators)
    plt.xlabel('Sample Length')
    plt.ylabel('n_Estimators')
    plt.title('Grid Search Results - Test Accuracy')
    plt.savefig(os.path.join(output_dir_2, 'grid_search_RF.png'))
    print('---- Ende GridSearch. ----')


# Hauptskript zum RF Test:
def testRF(data_raw, models, scaler, testdatensatz, saveData=False, conf_matrix=False):
    used_models = 'RF__' + models + r'/RF_' + scaler + 'Scaler'
    path = os.path.join(Config.PATH_RF, used_models)

    results = {}

    for filename in glob.glob(os.path.join(path, '*.joblib')):
        print('---------------------')

        # Extraktion von sample_length & n_estimators
        dateiname = os.path.basename(filename)
        print("Model: ", dateiname)

        teile = dateiname.split('_')
        n_estimators = int(teile[1])
        sample_length = int(teile[2])

        # Extraktion der Features
        features, labels = extractFeatures_MA_Karle(dataframe=data_raw, sample_length=sample_length)

        # Modell laden
        model = load(filename)

        # Modell vorhersagen machen
        predictions = model.predict(features)
        accuracy = accuracy_score(labels, predictions)
        label_order = ['Schritt_Zahnraeder', 'Schritt_Zahnriemen', 'Servo_Zahnraeder', 'Servo_Zahnriemen']
        report = classification_report(labels, predictions, labels=label_order)

        # Konfusionsmatrix
        cm = confusion_matrix(labels, predictions)

        if conf_matrix == True:
            # Erstellung der Konfusionsmatrix als Grafik
            plt.figure(figsize=(14, 10))
            ax = sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=label_order, yticklabels=label_order)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=90)
            plt.xlabel('Vorhergesagte Labels')
            plt.ylabel('Tatsächliche Labels')
            plt.title('Konfusionsmatrix')
            path_cm = r'RF__' + models + '\\RF_' + scaler + 'Scaler\\' + 'cm_plot_' + '_' + str(
                dateiname) + '_Test_' + str(testdatensatz) + '.png'
            plt.savefig(os.path.join(Config.PATH_RF, path_cm))
            print('\tKonfusionsmatrix erfolgreich abgespeichert.')

        # Ausgabe Ergebnisse
        print(f"\tTestaccuracy:\t{accuracy}")
        # print("Classification Report:\n", report)
        print('---------------------')

        # Dictionary mit model & accuracy erstellen
        results[dateiname] = accuracy

    # Dictionary als Excel speichern
    if saveData == True:
        results_df = pd.DataFrame(list(results.items()), columns=['Modellname', 'Accuracy'])
        excel_name = r'Results_Test/RF_results__Test' + str(
            testdatensatz) + '_Model' + models + '_' + scaler + 'Scaler.xlsx'
        path = os.path.join(Config.PATH_RF, excel_name)
        results_df.to_excel(path, index=False)
        print('Ergebnisse in Excel gespeichert.')
    else:
        print('Keine Speicherung der Auswertung.')

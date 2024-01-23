import numpy as np
import pandas as pd

# Funktion zum Features extrahieren:
def extractFeatures_Stock(dataframe, window_size):
    # Number of windows
    num_windows = len(dataframe) // window_size

    # Initializing lists to store the extracted features and labels for each window
    features = []
    labels = []

    for i in range(num_windows):
        # Extracting a window from the dataset
        window = dataframe.iloc[i * window_size:(i + 1) * window_size]

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


#########################################################################################################################

from scipy.signal import find_peaks
from scipy.fft import fft
from scipy.stats import skew

def extractFeatures_MA_Karle(dataframe, window_size):
    # Number of windows
    num_windows = len(dataframe) // window_size

    # Initializing lists to store the extracted features and labels for each window
    features = []
    labels = []

    for i in range(num_windows):
        # Extracting a window from the dataset
        window = dataframe.iloc[i * window_size:(i + 1) * window_size]

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
        #data_skewness_current = skew(data_current)
        #data_skewness_position = skew(data_position)

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


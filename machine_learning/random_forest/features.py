import numpy as np
import pandas as pd

# Funktion zum Features extrahieren:
def extractFeatures(data, window_size):
    # Number of windows
    num_windows = len(data) // window_size

    # Initializing lists to store the extracted features and labels for each window
    features = []
    labels = []

    for i in range(num_windows):
        # Extracting a window from the dataset
        window = data.iloc[i * window_size:(i + 1) * window_size]

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



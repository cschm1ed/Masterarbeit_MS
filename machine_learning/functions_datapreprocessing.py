import pandas as pd
import os
import numpy as np
from configurations.config import Config
from functions.general import getallPaths
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

# Funktion, welche die Daten labelt
def labelData(path,data):
    # Zuweisen von labels:
    with open(os.path.join(path, 'used_parts.txt'), 'r') as file:
        inhalt = file.read()
        if 'Servo' in inhalt and 'Zahnräder' in inhalt:
            data['label'] = 'Servo_Zahnraeder'
        elif 'Schritt' in inhalt and 'Zahnräder' in inhalt:
            data['label'] = 'Schritt_Zahnraeder'
        elif 'Servo' in inhalt and 'Zahnriemen' in inhalt:
            data['label'] = 'Servo_Zahnriemen'
        elif 'Schritt' in inhalt and 'Zahnriemen' in inhalt:
            data['label'] = 'Schritt_Zahnriemen'
    return data


# Datenvorverarbeitung:
def getParquetRaw(data_name, saveData = False):
    # Aufrufen aller Pfade im Ordner #fertig
    paths = getallPaths()
    combined_df = pd.DataFrame()

    print('---- Start: getParquetRaw ----')

    for path in paths:
        # Einlesen von Current
        data = pd.read_csv(os.path.join(path, 'current.csv'))
        # Einlese von Position
        data_position = pd.read_csv(os.path.join(path, 'position.csv'))

        # Interpolation der Positionswerte auf die Zeitstempel des Stromdatensatzes
        interpolated_position = np.interp(data['time_[s]'], data_position['time_[s]'], data_position['position_[mm]'])
        data['position_[mm]'] = interpolated_position

        # Kürzen der Daten (auf dieselbe Länge):
        data = data.iloc[:18600]

        # Labeln der Daten:
        data = labelData(data=data, path=path)

        # Zusammenfügen von allen Dataframes:
        combined_df = pd.concat([combined_df, data], ignore_index=True)

    # Ausgabe des gesamten Dataframes:
    #print(combined_df)
    print('---- End. ----')
    # Speichern des gesamten Dataframes in einer neuen .csv Datei:
    if saveData == True:
        output_pfad = os.path.join(Config.PATH_Trainingsdaten, 'output_' + data_name + '.parquet')
        # combined_df.to_csv(output_pfad, index=False)
        combined_df.to_parquet(output_pfad)

    return combined_df


# Skalierung der Daten:
def scaleData(raw_data, scaler_type):
    print('\t---- Start: scaleData ----')

    if isinstance(raw_data, pd.DataFrame) :
        data = raw_data
    elif isinstance(raw_data, str):
        data = pd.read_parquet(raw_data)
    else:
        print('Fehler. ---')

    # Auswahl des Scalers
    if scaler_type == 'MinMax':
        scaler = MinMaxScaler()
    elif scaler_type == 'Standard':
        scaler = StandardScaler()
    else:
        print('Falscher / kein Scaler ausgewählt! Möglich ist: "MinMax" oder "Standard".')

    # Auswahl der zu skalierenden Spalten
    columns_to_scale = ['time_[s]', 'current_[mA]', 'position_[mm]']
    # Skalierung der Spalten
    data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])
    print('\t---- Ende: scaleData ----')

    return data

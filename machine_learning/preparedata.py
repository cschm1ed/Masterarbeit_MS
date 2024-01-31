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

# Funktion zum Bereinigen der Stromdaten:
def cleanData(data_current):
    df = data_current
    # Berechnung des Interquartilsabstands (IQR)
    Q1 = df['current_[mA]'].quantile(0.2)
    Q3 = df['current_[mA]'].quantile(0.8)
    IQR = Q3 - Q1

    # Bestimmung der Schwellenwerte für Ausreißer
    faktor = 1.5
    untere_grenze = Q1 - faktor * IQR
    obere_grenze = Q3 + faktor * IQR

    # Identifizierung der Ausreißer
    ausreisser_indices = df[(df['current_[mA]'] < untere_grenze) | (df['current_[mA]'] > obere_grenze)].index

    # Entfernen der Ausreißer
    df_ohne_ausreisser = df.drop(ausreisser_indices)

    # Rückgabe des Dataframes ohne Ausreißer
    return df_ohne_ausreisser


# Datenvorverarbeitung:
def prepareData(scaler_type, saveData = False):
    paths = getallPaths()
    combined_df = pd.DataFrame()

    print('---- Start: prepareData ----')
    print('Scaler: ' + scaler_type)

    if scaler_type == 'MinMax':
        scaler = MinMaxScaler()
    elif scaler_type == 'Standard':
        scaler = StandardScaler()
    else:
        print('Falscher / kein Scaler ausgewählt! Möglich ist: "MinMax" oder "Standard".')

    for path in paths:
        # Current:
        data = pd.read_csv(os.path.join(path, 'current.csv'))
        # Position:
        data_position = pd.read_csv(os.path.join(path, 'position.csv'))
        # Interpolation der Positionswerte auf die Zeitstempel des Stromdatensatzes:
        interpolated_position = np.interp(data['time_[s]'], data_position['time_[s]'], data_position['position_[mm]'])
        data['position_[mm]'] = interpolated_position

        # Normalisierung / Skalierung:
        data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

        # Kürzen der Daten (auf dieselbe Länge):
        data = data.iloc[:18600]

        # Labeln der Daten:
        data = labelData(data=data, path=path)

        # Zusammenfügen von allen Dataframes:
        combined_df = pd.concat([combined_df, data], ignore_index=True)

    # Ausgabe des gesamten Dataframes:
    print(combined_df)
    print('---- End. ----')
    # Speichern des gesamten Dataframes in einer neuen .csv Datei:
    if saveData == True:
        output_pfad = os.path.join(Config.PATH_data_machine_learning, 'output_Testdatensatz_3_' + scaler_type + 'Scaler.parquet')
        # combined_df.to_csv(output_pfad, index=False)
        combined_df.to_parquet(output_pfad)

    return combined_df

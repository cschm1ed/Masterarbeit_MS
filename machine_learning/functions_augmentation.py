import pandas as pd
import os
from configurations.config import Config
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import random
from sklearn.preprocessing import StandardScaler

# Funktionen zur Erzeugung von synthetischen Daten:
####################################################################################

# Funktion zur Erzeugung der Interpolationsfunktion:
def createIntFunktion():
    data_old = pd.read_csv(r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Training\#_servo_zahnriemen\2023-12-12_10-23-19\current.csv')
    data_new = pd.read_csv(r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Testdatensatz_2\#_servo_zahnriemen\2024-01-29_19-33-29\current.csv')

    data = data_new['current_[mA]'] - data_old['current_[mA]']

    dfs = [data, data_new['time_[s]']]
    data = pd.concat(dfs, axis = 1)
    data = data.iloc[:18600]
    data_old = data_old.iloc[:18600]

    # Datenpunkte
    step_size = 120/18599
    x = np.arange(0, 120 + step_size, step_size)
    y = np.array(data['current_[mA]'])

    # Erstellen der Interpolationsfunktion
    p = interp1d(x, y, kind='cubic')

    return p


# Funktion zur Erzeugung der synthetischen Daten, basierend auf einer Funktion p

def createAugData(p, number_runs, factor_down=0.2, factor_up=1.8):
    print('---- Start: Erstellung synthetischer Daten ----')
    # Einlesen der Rohdatei
    raw_path = os.path.join(Config.PATH_Trainingsdaten, r'output_raw_18600.parquet')
    df = pd.read_parquet(raw_path)

    print('Rohdatei: ' + raw_path)

    # Parameter festlegen / erstellen
    combined_df = pd.DataFrame()
    num = len(df) // 18600

    for i in range(number_runs):
        for i in range(num):
            factor = random.uniform(factor_down, factor_up)
            window = df.iloc[i * 18600:(i + 1) * 18600]
            window = window.reset_index(drop=True)

            x_new = np.array(window['time_[s]'])
            y_help = np.array(window['current_[mA]'])
            y_new = p(x_new) * factor + y_help

            data_aug = pd.DataFrame(x_new, columns=['time_[s]'])
            data_aug['current_[mA]'] = pd.DataFrame(y_new)
            data_aug['position_[mm]'] = window['position_[mm]']
            data_aug['label'] = window['label']

            # Hinzufügen zum kombinierten Dataframe
            combined_df = pd.concat([combined_df, data_aug], ignore_index=True)

    # Speichern der neuen synthetischen Daten
    combined_df.to_parquet(os.path.join(Config.PATH_Trainingsdaten, r'output_aug_18600.parquet'))
    print('\tDatei erfolgreich abgespeichert.')
    print('---- Ende. ----')

# Zusammenfügen von raw- + aug-.parquet Dateien
def combineRawAug(data_raw, data_aug):
    # data_raw = pd.read_parquet(
    #     r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert\raw_data_sorted\#machine_learning\Trainingsdaten\output_raw_18600.parquet')
    # data_aug = pd.read_parquet(
    #     r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert\raw_data_sorted\#machine_learning\Trainingsdaten\output_aug_18600.parquet')

    combined_df = pd.DataFrame

    combined_df = pd.concat([data_raw, data_aug], ignore_index=True)

    combined_df.to_parquet(os.path.join(Config.PATH_Trainingsdaten, r'output_raw+aug_18600.parquet'))

    return combined_df
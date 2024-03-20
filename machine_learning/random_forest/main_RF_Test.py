from machine_learning.random_forest.functions_rf import *
from machine_learning.functions_datapreprocessing import scaleData
from configurations.config import Config
import os

# ----
# MAIN: TESTEN EINES RF-MODELLS
# ----

##############################################################
# EINGABEN:

# Auswahl des Testdatensatzes:
# 1: andere Ref.-fahrt mit Gewicht m=2.5kg
# 2: selbe Ref.-fahrt mit Gewicht m=2.5kg
# Train: alte Ref.-fahrt ohne Gewicht (Trainingsdaten)
# testdatensatz = '1'
#testdatensatze = [1, 2]
testdatensatze = ['Train']

# Auswahl der Modelle:
# aus Train Daten: r'output_raw_18600.parquet'
# aus allen Daten: r'output_raw+aug+aug_new2_18600.parquet'
# models = r'output_raw_18600.parquet'
models = r'output_raw+aug+aug_new2_18600.parquet'

# MinMax, Standard oder No
# scaler = 'No'
# scalers = ['No', 'Standard', 'MinMax']
scalers = ['Standard']

##############################################################


for scaler in scalers:
    for testdatensatz in testdatensatze:
        # Einlesen der Rohdatei
        raw_data_name = r'output_Testdatensatz_' + str(testdatensatz) + '_raw.parquet'
        df = os.path.join(Config.PATH_Testdaten, raw_data_name)
        data = pd.read_parquet(df)

        print('---- Start: Testdaten durch RF-Modell klassifizieren ----')
        print('Testdatensatz:\t' + raw_data_name)

        # Skalierung der Daten:
        if scaler == 'MinMax' or scaler == 'Standard':
            data = scaleData(raw_data=data, scaler_type=scaler)
            print('Skalierung: ' + scaler)
        elif scaler == 'No':
            print('Keine Skalierung.')
        else:
            print('Fehler bei der Auswahl des Scalers.')
        print('---------------------')

        testRF(data_raw=data, models=models, scaler=scaler, testdatensatz=testdatensatz, saveData=False,
               conf_matrix=True)

        print('---- Ende. ----')

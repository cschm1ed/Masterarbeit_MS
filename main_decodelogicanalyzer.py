import pandas as pd
from datetime import datetime
import functions_decodedata



# Dateipfad zur CSV-Datei
dateinamen = [

    'raw_data_sorted/test_LogicAnalyzer/digital.csv',
    'raw_data_sorted/test_LogicAnalyzer/4cm.csv',
    'raw_data_sorted/test_LogicAnalyzer/-4cm.csv',
    'raw_data_sorted/test_LogicAnalyzer/20cm_1.csv',
    'raw_data_sorted/test_LogicAnalyzer/-20cm_1.csv',
    'raw_data_sorted/test_LogicAnalyzer/mehrals4cm.csv',
    'raw_data_sorted/test_LogicAnalyzer/-mehrals4cm.csv',
    'raw_data_sorted/test_LogicAnalyzer/20cm_2.csv',
    'raw_data_sorted/test_LogicAnalyzer/-20cm_2.csv',
    'raw_data_sorted/test_LogicAnalyzer/52cm.csv',
    'raw_data_sorted/test_LogicAnalyzer/-52cm.csv',
    'raw_data_sorted/test_LogicAnalyzer/-52cm_2.csv'
]

for dateiname in dateinamen:
    aktuelle_zeit = datetime.now().strftime('%H:%M:%S')
    print('---- Start: ' + str(aktuelle_zeit))
    print(dateiname)

    # Einlesen in ein Pandas DataFrame
    df = pd.read_csv(dateiname)

    # Aufrufen der Funktionen
    result = functions_decodedata.decodePosition(df)

    # Ausgabe des Ergebnis Dataframes
    print(result)

    aktuelle_zeit = datetime.now().strftime('%H:%M:%S')
    print('---- Ende: ' + str(aktuelle_zeit) + ' ----')





from keras.models import load_model
from configurations.config import Config
import os
import pandas as pd
from machine_learning.knn.functions_knn import *
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from machine_learning.functions_datapreprocessing import scaleData

##################################################################
# Eingaben:

# Auswahl des Testdatensatzes:
# 1: andere Ref.-fahrt mit Gewicht m=2.5kg
# 2: selbe Ref.-fahrt mit Gewicht m=2.5kg
# Train: alte Ref.-fahrt ohne Gewicht (Trainingsdaten)
testdatensatz = 'Train'

# Auswahl der Modells:
# model_LSTM_Standard_TrainData.h5/.keras
# model_LSTM_Standard_AugData.h5/.keras
# model_LSTM_Standard_TrainAugData.h5/.keras
version = 'TrainAug'
model_name = r'model_LSTM_Standard_' + version + 'Data.h5'


# MinMax oder Standard
scaler = 'Standard'
sample_length = 25

##################################################################

# Einlesen der Rohdatei
raw_data_name = r'output_Testdatensatz_' + str(testdatensatz) + '_raw.parquet'
data_raw = os.path.join(Config.PATH_Testdaten, raw_data_name)
df = pd.read_parquet(data_raw)

print('---- Start: Testdaten durch Modell klassifizieren ----')
print('Testdatensatz:\t' + raw_data_name)
print('Modell:\t \t    ' + model_name)

# Skalierung der Daten
data = scaleData(raw_data=df, scaler_type=scaler)

# Laden des Modells
model_path = os.path.join(r'Modelle/', model_name)
pfad = os.path.join(Config.PATH_KNN, model_path)
model = load_model(pfad)

# Anwender der Testdaten auf das Modell
test_accuracy = testLSTM(data=data, model=model, sample_length=sample_length, raw_data_name=raw_data_name,
                         model_name=model_name)

print(f"\tTestaccuracy: {test_accuracy}")

print('---- Ende. ----')

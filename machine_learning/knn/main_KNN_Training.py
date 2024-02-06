# für Nutzung von Google Colab
# from google.colab import drive
# drive.mount('/content/drive')
# import sys
# sys.path.append('/content/drive/MyDrive/Colab/Masterarbeit_Schubert')

from machine_learning.knn.functions_knn import *
from machine_learning.functions_datapreprocessing import *
from configurations.config import Config
import os

# ----
# MAIN: TRAINING EINES KNNs
# ----


##############################################################
# EINGABEN:

# Name der Trainingsdatei
data_training = r'output_raw_18600.parquet'

# MinMax oder Standard
scaler = 'Standard'

# Hyperparameter für StandardScaler Modell
epochs = 1
sample_length = 25
batch_size = 128
learning_rate = 0.001

##############################################################


print('---- Start Training KNN: ----')
print('Rohdatei: ' + data_training)
print(f'Sample Length: {sample_length}, Batch Size: {batch_size}, Learning Rate: {learning_rate}')

print('---------------------')
# Einlesen + Skalieren der Daten
path = os.path.join(Config.PATH_Trainingsdaten, data_training)
data = scaleData(raw_data=path, scaler_type=scaler)
print('---------------------')

# Hauptfunktion
test_accuracy, model = trainLSTM(data=data, sample_length=sample_length, batch_size=batch_size, epochs=epochs,
                                 learning_rate=learning_rate, scaler=scaler)

print(f"\tTesaccuracy: {test_accuracy}")

print('---- Ende. ----')

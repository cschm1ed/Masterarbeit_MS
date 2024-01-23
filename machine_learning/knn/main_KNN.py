# für Nutzung von Google Colab
# from google.colab import drive
# drive.mount('/content/drive')
# import sys
# sys.path.append('/content/drive/MyDrive/Colab/Masterarbeit_Schubert')


from machine_learning.knn.functions_knn import *
from configurations.config import Config
import matplotlib.pyplot as plt
import os
import numpy as np

if __name__ == "__main__":
    # Rohdatei
    raw_data = 'output_MinMaxScaler.parquet'

    # Parameter
    sample_length = 50
    batch_size = 64

    # Feste Parameter
    learning_rate = 0.001
    epochs = 300

    print('---- Start Training: ----')
    print('Rohdatei: ' + raw_data)
    print('---------------------')
    print(f'\tSample Length: {sample_length}, Batch Size: {batch_size}, Learning Rate: {learning_rate}')

    # Hauptfunktion
    accuracy, model = main_LSTM(sample_length=sample_length, batch_size=batch_size, epochs=epochs,
                                learning_rate=learning_rate, raw_data=raw_data)
    model.save(os.path.join(Config.PATH_data_machine_learning, 'model_LSTM_Standard.h5'))

    print(f"\tAccuracy: {accuracy}")

    print('---- Ende. ----')
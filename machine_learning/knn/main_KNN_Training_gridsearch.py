# from google.colab import drive
# drive.mount('/content/drive')
# import sys
# sys.path.append('/content/drive/MyDrive/Colab/Masterarbeit_Schubert')

from configurations.config import Config
import matplotlib.pyplot as plt
import os
import numpy as np

# ----
# MAIN: TRAINING EINES RANDOM FORESTS
# ----


##############################################################
# EINGABEN:

# Rohdatei
raw_data = 'output_MinMaxScaler.parquet'

# Parameter für Grid Search
sample_lengths = [25, 50, 100, 200]
batch_sizes = [16, 32, 64, 128]

##############################################################


num_combinations = len(sample_lengths) * len(batch_sizes)
grid = np.zeros((len(batch_sizes), len(sample_lengths)))

# Feste Parameter
learning_rate = 0.001
epochs = 1
n = 1
results = {}

print('---- Start GridSearch: ----')
print('Rohdatei: ' + raw_data)
# Grid Search durchführen
for i, batch_size in enumerate(batch_sizes):
    for j, sample_length in enumerate(sample_lengths):
        print('_________________________________________________________________')
        print(f'\tAnzahl Durchläufe: ' + str(n) + ' / ' + str(num_combinations))
        print(f'\tSample Length: {sample_length}, Batch Size: {batch_size}, Learning Rate: {learning_rate}')

        # Hauptfunktion
        accuracy, model = main_LSTM(sample_length=sample_length, batch_size=batch_size, epochs=epochs,
                                    learning_rate=learning_rate, raw_data=raw_data)
        results[(sample_length, batch_size)] = accuracy

        n += 1
        print(f"\tAccuracy: {accuracy}")
        print('_________________________________________________________________')

        grid[i, j] = accuracy

# Ausgabe gridsearch
plt.figure(figsize=(8, 6))
plt.imshow(grid, cmap='Blues', interpolation='nearest')

for i in range(len(batch_sizes)):
    for j in range(len(sample_lengths)):
        plt.text(j, i, f'{grid[i, j] * 100:.2f}%', ha='center', va='center', color='black')

plt.colorbar(label='Test Accuracy')
plt.xticks(np.arange(len(sample_lengths)), sample_lengths)
plt.yticks(np.arange(len(batch_sizes)), batch_sizes)
plt.xlabel('Sample Length')
plt.ylabel('Batch Size')
plt.title('Grid Search Results - Test Accuracy')
plt.savefig(os.path.join(Config.PATH_data_machine_learning, 'grid_search_LSTM.png'))
print('---- Ende GridSearch. ----')

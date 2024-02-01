import pandas as pd
from configurations.config import Config
import numpy as np
import matplotlib.pyplot as plt
import re
import os

#todo: muss noch komplett aktualisiert werden

file_path = os.path.join(Config.PATH_KNN, Config.STR_MinMaxScaler)
results = {}

for ordnername in os.listdir(file_path):
    ordner_pfad = os.path.join(file_path, ordnername)
    path_txt = os.path.join(ordner_pfad, 'model_summary.txt')

    with open(path_txt, 'r') as file:
        text = file.read()

    # Regex Patterns
    batchgroesse_pattern = r"Batchgroessse: (\d+)"
    sample_laenge_pattern = r"Sample Laenge: (\d+)"
    accuracy_testdaten_pattern = r"Accuracy auf Testdaten: ([0-9.]+)"

    # Extrahiere Werte
    batchgroesse = int(re.findall(batchgroesse_pattern, text)[0])
    sample_laenge = int(re.findall(sample_laenge_pattern, text)[0])
    accuracy_testdaten = float(re.findall(accuracy_testdaten_pattern, text)[0])

    # Ausgabe der extrahierten Werte
    #print(f"Batchgroessse: {batchgroesse}")
    #print(f"Sample Länge: {sample_laenge}")
    #print(f"Accuracy auf Testdaten: {accuracy_testdaten}")

    results[(batchgroesse, sample_laenge)] = accuracy_testdaten

# Extrahieren der batchgroessen und sample_laengen
batchgroessen = set()
sample_laengen = set()

for key in results.keys():
    batchgroesse, sample_laenge = key
    batchgroessen.add(batchgroesse)
    sample_laengen.add(sample_laenge)

# Konvertieren in Listen
batch_sizes = list(batchgroessen)
sample_lengths = list(sample_laengen)

# Optional: Listen sortieren, wenn notwendig
batch_sizes.sort()
sample_lengths.sort()

# Ausgabe der Listen
print("Batchgroessen:", batch_sizes)
print("Sample Laengen:", sample_lengths)


# Initialisieren der Grid-Matrix
grid = np.zeros((len(batch_sizes), len(sample_lengths)))

# Füllen der Grid-Matrix mit den Werten aus 'results'
for i, batch_size in enumerate(batch_sizes):
    for j, sample_length in enumerate(sample_lengths):
        grid[i, j] = results.get((batch_size, sample_length), 0)  # Standardwert ist 0

# Erstellen des Heatmap-Diagramms
plt.figure(figsize=(8, 6))
plt.imshow(grid, cmap='Blues', interpolation='nearest')

# Hinzufügen von Text in jede Zelle für die Genauigkeit
for i in range(len(batch_sizes)):
    for j in range(len(sample_lengths)):
        plt.text(j, i, f'{grid[i, j] * 100:.2f}%', ha='center', va='center', color='black')

# Hinzufügen weiterer Diagrammdetails
plt.colorbar(label='Test Accuracy')
plt.xticks(np.arange(len(sample_lengths)), sample_lengths)
plt.yticks(np.arange(len(batch_sizes)), batch_sizes)
plt.xlabel('Sample Length')
plt.ylabel('Batch Size')
plt.title('Grid Search Results - Test Accuracy')
#plt.show()
# Speichern des Diagramms
plt.savefig(os.path.join(Config.PATH_KNN, 'grid_search_LSTM_MinMax.png'))


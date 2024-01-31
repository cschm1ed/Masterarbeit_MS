from keras.models import load_model
from configurations.config import Config
import os
import pandas as pd
from machine_learning.knn.functions_knn import *
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

##################################################################

# Eingaben:
#1: andere Ref.-fahrt; 2: selbe Ref.-fahrt mit Gewicht m=2.5kg; 3: noch erstellen
testdatensatz = 3
#MinMax oder Standard
scaler = 'MinMax'

##################################################################

# Einlesen der Rohdatei
raw_data = r'output_Testdatensatz_' + str(testdatensatz) + '_' + scaler + 'Scaler.parquet'
data_raw = os.path.join(Config.PATH_Testdaten, raw_data)
df = pd.read_parquet(data_raw)

if scaler == 'MinMax':
    sample_length = 50
    model_path = r'LSTM/MinMaxScaler/FINAL/model_LSTM_MinMax.h5'
elif scaler == 'Standard':
    sample_length = 25
    model_path = r'LSTM/StandardScaler/FINAL/model_LSTM_Standard.h5'
else:
    print('Fehler. ---')

# Datenvorverarbeiten
X, y, label_encoder = preprocess_data(df)
sample_length, features = sample_length, 2
X, y = prepare_lstm_data(X=X, y=y, sample_length=sample_length,
                         features=features)

# Modellparameter
input_shape = (sample_length, features)
num_classes = 4

# Konvertieren der Labels in One-Hot-Kodierung
y_test_one_hot = to_categorical(y, num_classes=num_classes)

# Laden des Modells
pfad = os.path.join(Config.PATH_KNN, model_path)
model = load_model(pfad)

# Angenommen, `x_test` und `y_test` sind Ihre Testdaten und -labels
score = model.evaluate(X, y_test_one_hot, verbose=0)
print('Testverlust:', score[0])
print('Testgenauigkeit:', score[1])


predictions = model.predict(X)
predicted_labels = np.argmax(predictions, axis=1)
true_labels = np.argmax(y_test_one_hot, axis=1)


# Grafische Ausgaben:

# Erstellen der Konfusionsmatrix
cm = confusion_matrix(true_labels, predicted_labels)

# Konfusionsmatrix plotten
# Konfusionsmatrix grafisch darstellen
plt.figure(figsize=(14, 10))
sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel('Vorhergesagte Labels')
plt.ylabel('Wahre Labels')
plt.title('Konfusionsmatrix')
matrix_path = r'LSTM/' + scaler + 'Scaler/Testdaten/confusion_matrix_plot_Testdatensatz_' + str(testdatensatz) + '.png'
output_dir = os.path.join(Config.PATH_KNN, matrix_path)
plt.savefig(output_dir)
#plt.show()

# txt Datei mit Model Summary speichern
txt_file_path = os.path.join(Config.PATH_KNN, r'LSTM/' + scaler + 'Scaler/Testdaten/model_summary_Testdatensatz_' + str(testdatensatz) + '.txt')

# Öffnen der Datei im Schreibmodus ('w' für Schreiben)
with open(txt_file_path, 'w') as file:
    file.write('\n')
    file.write('_________________________________________________________________\n')
    # Hyperparameter
    file.write('Testverlust: {}\n'.format(score[0]))
    file.write('Testgenauigkeit: {}\n'.format(score[1]))
    file.write('_________________________________________________________________\n')
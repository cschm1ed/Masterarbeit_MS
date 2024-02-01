
import pandas as pd
from sklearn.preprocessing import LabelEncoder

################################################################################################################################
# Datenvorverarbeitung

data_raw = r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert\raw_data_sorted\#machine_learning\output_MinMaxScaler.parquet'
#data_raw = r'/content/drive/MyDrive/Colab/output_MinMaxScaler.parquet'
df = pd.read_parquet(data_raw)

# Labels auf Zahlen setzen
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(df['label'])
df['label'] = encoded_labels
# Ausgabe der neuen Labels
label_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
print(label_mapping)

# Trennen von Features und Label
df = df.drop('time_[s]', axis=1)
X = df.drop('label', axis=1)
y = df['label']

# Datenformat für KNN anpassen
sample_length = 100
samples = int(18600*81/sample_length)
features = 2
X_reshaped = X.values.reshape(samples, sample_length, features)
y_reshaped = df['label'].iloc[::sample_length].reset_index(drop=True)

################################################################################################################################


from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization

# LSTM

X = X_reshaped
y = y_reshaped

# Aufteilen der Daten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=42, stratify=y_train)


# Konvertieren der Labels in One-Hot-Kodierung
y_train_one_hot = to_categorical(y_train, num_classes=4)
y_test_one_hot = to_categorical(y_test, num_classes=4)
y_val_one_hot = to_categorical(y_val, num_classes=4)

# Modellparameter
input_shape = (sample_length, features)
num_classes = 4


# Aufbau des Modells:
model = Sequential()

# Add the first LSTM layer with 50 units and input shape (time_steps, features)
model.add(LSTM(50, return_sequences=True, input_shape=(sample_length, features)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
# Add a second LSTM layer with 50 units
model.add(LSTM(150, return_sequences=True))
model.add(BatchNormalization())
model.add(Dropout(0.4))
# Add a third LSTM layer with 50 units
model.add(LSTM(150, return_sequences=True))
model.add(BatchNormalization())
model.add(Dropout(0.4))
# Add a fourth LSTM layer with 50 units
model.add(LSTM(50))
model.add(BatchNormalization())
model.add(Dropout(0.4))
# Add a dense layer with the number of output neurons
model.add(Dense(4, activation='softmax'))


# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Print a summary of the model architecture
model.summary()

# Modell Trainieren
batch_size = 16
epochs = 1
history = model.fit(X_train, y_train_one_hot, validation_data=(X_val, y_val_one_hot), epochs=epochs, batch_size=batch_size)

# Modell Evaluieren
model.evaluate(X_test, y_test_one_hot)


################################################################################################################################
################################################################################################################################
import os
from configurations.config import Config
from datetime import datetime



# Speciherung der wichtigsten Daten

ordnername = Config.PATH_KNN
output_dir = os.path.join(ordnername, datetime.now().strftime("%Y%m%d_%H%M%S"))
os.makedirs(output_dir)

# txt Datei mit Model Summary speichern
txt_file_path = os.path.join(output_dir, 'model_summary.txt')

lr = model.optimizer.learning_rate.numpy()

# Öffnen der Datei im Schreibmodus ('w' für Schreiben)
with open(txt_file_path, 'w') as file:
    model.summary(print_fn=lambda x: file.write(x + '\n'))
    file.write('\n')

    # Hyperparameter
    file.write('Hyperparameter:\n')
    # Hier die Hyperparameter manuell hinzufügen, z.B.:
    file.write('Lernrate: {}\n'.format(lr))
    file.write('Batchgroessse: {}\n'.format(batch_size))
    file.write('Epochen: {}\n'.format(epochs))
    file.write('\n')

    # Datum und Uhrzeit
    file.write('Datum und Uhrzeit des Trainings: {}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

from sklearn.metrics import classification_report, confusion_matrix
import json


# Bericht
report_file_path = os.path.join(output_dir, 'training_report.txt')

with open(report_file_path, 'w') as file:

    # Trainings- und Validierungsmetriken
    file.write('Trainings- und Validierungsmetriken:\n')
    file.write(json.dumps(history.history, indent=4))
    file.write('\n')

    # todo: Weiteres hinzufügen + dann GridSearch

    # Datum und Uhrzeit
    file.write('Datum und Uhrzeit des Trainings: {}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


################################################################################################################################
import matplotlib.pyplot as plt

# Grafische Ausgabe

# Erstellen und Speichern der Genauigkeitsgrafik
plt.figure(figsize=(6, 4))
plt.plot(history.history['accuracy'], label='Trainingsgenauigkeit')
plt.plot(history.history['val_accuracy'], label='Validierungsgenauigkeit')
plt.title('Genauigkeit über Epochen')
plt.xlabel('Epochen')
plt.ylabel('Genauigkeit')
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, 'accuracy_plot.png'))

# Erstellen und Speichern der Verlustgrafik
plt.figure(figsize=(6, 4))
plt.plot(history.history['loss'], label='Trainingsverlust')
plt.plot(history.history['val_loss'], label='Validierungsverlust')
plt.title('Verlust über Epochen')
plt.xlabel('Epochen')
plt.ylabel('Verlust')
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, 'loss_plot.png'))

# Anzeigen beider Grafiken
plt.figure(figsize=(12, 4))

# Genauigkeit
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Trainingsgenauigkeit')
plt.plot(history.history['val_accuracy'], label='Validierungsgenauigkeit')
plt.title('Genauigkeit über Epochen')
plt.xlabel('Epochen')
plt.ylabel('Genauigkeit')
plt.legend()
plt.grid()

# Verlust
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Trainingsverlust')
plt.plot(history.history['val_loss'], label='Validierungsverlust')
plt.title('Verlust über Epochen')
plt.xlabel('Epochen')
plt.ylabel('Verlust')
plt.legend()
plt.grid()

plt.show()
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization
from keras.optimizers import Adam
from configurations.config import Config
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def read_data(filepath):
    try:
        df = pd.read_parquet(filepath)
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None
    return df


def preprocess_data(df):
    label_encoder = LabelEncoder()
    df['label'] = label_encoder.fit_transform(df['label'])
    label_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
    # print(label_mapping)
    df = df.drop('time_[s]', axis=1)
    X = df.drop('label', axis=1)
    y = df['label']
    return X, y, label_encoder


def prepare_lstm_data(X, y, sample_length, features):
    samples = int(18600 * 81 / sample_length)
    X_reshaped = X.values.reshape(samples, sample_length, features)
    y_reshaped = y.iloc[::sample_length].reset_index(drop=True)
    return X_reshaped, y_reshaped


def build_lstm_model(input_shape, num_classes, learning_rate):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        BatchNormalization(), Dropout(0.4),
        LSTM(150, return_sequences=True),
        BatchNormalization(), Dropout(0.4),
        LSTM(150, return_sequences=True),
        BatchNormalization(), Dropout(0.4),
        LSTM(50),
        BatchNormalization(), Dropout(0.4),
        Dense(num_classes, activation='softmax')
    ])
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def save_data_lstm(model, history, batch_size, epochs, cm, label_encoder, test_loss, test_accuracy, sample_length,
                   learning_rate):
    ordnername = 'batchsize_' + str(batch_size) + '__samplelength_' + str(sample_length) + '__learningrate_' + str(
        learning_rate) + '__' + datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = os.path.join(Config.PATH_KNN, ordnername)
    os.makedirs(output_dir)

    # txt Datei mit Model Summary speichern
    txt_file_path = os.path.join(output_dir, 'model_summary.txt')

    # Öffnen der Datei im Schreibmodus ('w' für Schreiben)
    with open(txt_file_path, 'w') as file:
        # Modelleigenschaften
        model.summary(print_fn=lambda x: file.write(x + '\n'))
        file.write('\n')
        # Hyperparameter
        file.write('Hyperparameter:\n')
        file.write('learning_rate: {}\n'.format(learning_rate))
        file.write('batch_size: {}\n'.format(batch_size))
        file.write('epochs: {}\n'.format(epochs))
        file.write('sample_length: {}\n'.format(sample_length))
        file.write('\n\n')
        file.write('_________________________________________________________________\n')
        file.write('_________________________________________________________________\n')
        # Resultate
        file.write('Results:\n')
        file.write("Accuracy auf Trainingsdaten: {}\n".format(history.history['accuracy'][-1]))
        file.write("Loss auf Trainingsdaten: {}\n".format(history.history['loss'][-1]))
        file.write("Accuracy auf Validierungsdaten: {}\n".format(history.history['val_accuracy'][-1]))
        file.write("Loss auf Validierungsdaten: {}\n".format(history.history['val_loss'][-1]))
        file.write('\n')
        file.write("Accuracy auf Testdaten: {}\n".format(test_accuracy))
        file.write("Loss auf Testdaten: {}\n".format(test_loss))

        file.write('\n\n')
        file.write('_________________________________________________________________\n')
        file.write('_________________________________________________________________\n')
        # Datum und Uhrzeit
        file.write('Datum und Uhrzeit des Trainings: {}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    ##########
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

    # Konfusionsmatrix grafisch darstellen
    plt.figure(figsize=(14, 10))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=label_encoder.classes_,
                yticklabels=label_encoder.classes_)
    plt.xlabel('Vorhergesagte Labels')
    plt.ylabel('Wahre Labels')
    plt.title('Konfusionsmatrix')
    plt.savefig(os.path.join(output_dir, 'confusion_matrix_plot.png'))


# Hauptteil des Skripts
def main_LSTM(sample_length, batch_size, epochs, learning_rate, raw_data):
    # Einlesen der Rohdatei
    data_raw = os.path.join(Config.PATH_data_machine_learning, raw_data)
    df = read_data(data_raw)
    if df is not None:
        # Datenvorverarbeiten
        X, y, label_encoder = preprocess_data(df)
        sample_length, features = sample_length, 2
        X, y = prepare_lstm_data(X=X, y=y, sample_length=sample_length,
                                 features=features)
        # Aufteilen der Daten
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=42,
                                                          stratify=y_train)

        # Modellparameter
        input_shape = (sample_length, features)
        num_classes = 4

        # Konvertieren der Labels in One-Hot-Kodierung
        y_train_one_hot = to_categorical(y_train, num_classes=num_classes)
        y_test_one_hot = to_categorical(y_test, num_classes=num_classes)
        y_val_one_hot = to_categorical(y_val, num_classes=num_classes)

        # Bau des Netzes
        model = build_lstm_model(input_shape, num_classes, learning_rate)

        # Fit des Netzes
        history = model.fit(X_train, y_train_one_hot, validation_data=(X_val, y_val_one_hot), epochs=epochs,
                            batch_size=batch_size)

        # Modell Evaluieren
        test_loss, test_accuracy = model.evaluate(X_test, y_test_one_hot)

        # Modellvorhersagen machen
        y_pred = model.predict(X_test)
        y_pred_classes = y_pred.argmax(axis=1)
        # Umkehrung des Label Encodings
        y_pred_labels = label_encoder.inverse_transform(y_pred_classes)
        y_test_labels = label_encoder.inverse_transform(y_test)

        # Konfusionsmatrix berechnen
        cm = confusion_matrix(y_test_labels, y_pred_labels)

        # Daten abspeichern
        save_data_lstm(model=model, history=history, batch_size=batch_size,
                       epochs=epochs, cm=cm, label_encoder=label_encoder,
                       test_loss=test_loss, test_accuracy=test_accuracy, sample_length=sample_length,
                       learning_rate=learning_rate)
        return test_accuracy

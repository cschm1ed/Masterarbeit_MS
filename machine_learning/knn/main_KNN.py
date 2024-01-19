import machine_learning.knn.functions_knn
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix


# Hauptteil des Skripts
def main_LSTM(sample_length=100, batch_size=16, epochs=10):
    data_raw = r'C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\PycharmProjects\Masterarbeit_Schubert\raw_data_sorted\#machine_learning\output_MinMaxScaler.parquet'
    # data_raw = r'/content/drive/MyDrive/Colab/output_MinMaxScaler.parquet'
    df = machine_learning.knn.functions_knn.read_data(data_raw)
    if df is not None:
        X, y, label_encoder = machine_learning.knn.functions_knn.preprocess_data(df)
        sample_length, features = sample_length, 2
        X, y = machine_learning.knn.functions_knn.prepare_lstm_data(X=X, y=y, sample_length=sample_length,
                                                                    features=features)
        # Aufteilen der Daten
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=42,
                                                          stratify=y_train)
        # Konvertieren der Labels in One-Hot-Kodierung
        y_train_one_hot = to_categorical(y_train, num_classes=4)
        y_test_one_hot = to_categorical(y_test, num_classes=4)
        y_val_one_hot = to_categorical(y_val, num_classes=4)

        # Modellparameter
        input_shape = (sample_length, features)
        num_classes = 4

        # Bau des Netzes
        model = machine_learning.knn.functions_knn.build_lstm_model(input_shape, num_classes)

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
        machine_learning.knn.functions_knn.save_data_lstm(model=model, history=history, batch_size=batch_size,
                                                          epochs=epochs, cm=cm, label_encoder=label_encoder,
                                                          test_loss=test_loss, test_accuracy=test_accuracy)




if __name__ == "__main__":

    main_LSTM(sample_length=100, batch_size=1024, epochs=1)

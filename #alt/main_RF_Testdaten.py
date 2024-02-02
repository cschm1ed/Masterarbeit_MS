from configurations.config import Config
import os
import glob
import re
from joblib import load
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns

##################################################################

# Eingaben:
# 1: andere Ref.-fahrt; 2: selbe Ref.-fahrt mit Gewicht m=2.5kg; 3: noch erstellen
testdatensatz = 3
# No, MinMax oder Standard
scaler = 'Standard'

##################################################################

# Einlesen der Rohdatei
raw_data = r'output_Testdatensatz_' + str(testdatensatz) + '_' + scaler + 'Scaler.parquet'
data_raw = os.path.join(Config.PATH_Testdaten, raw_data)
df = pd.read_parquet(data_raw)

# Auswahl des Modells
scaler_raw = scaler + 'Scaler'
path = os.path.join(Config.PATH_RF, scaler_raw)

for filename in glob.glob(os.path.join(path, '*.joblib')):
    print("Model:", filename)
    match = re.search(r'(\d+)\.joblib', filename)
    if match:
        # Konvertieren der gefundenen Zeichenkette in eine Zahl und Hinzufügen zur Liste
        sample_length = int(match.group(1))

    match2 = re.search(r'random_forest_(\d+)_\d+\.joblib', filename)
    if match2:
        n_estimators = int(match2.group(1))

    # Extraktion der Features
    features, labels = extractFeatures_MA_Karle(dataframe=df, sample_length=sample_length)

    # Modell laden
    model = load(filename)

    predictions = model.predict(features)
    accuracy = accuracy_score(labels, predictions)
    report = classification_report(labels, predictions)

    print('Testgenauigkeit:', accuracy)
    #print("Classification Report:\n", report)

    # Grafische Ausgaben:

    # Erstellen der Konfusionsmatrix
    # Berechnung der Konfusionsmatrix
    cm = confusion_matrix(labels, predictions)

    # Visualisierung der Konfusionsmatrix
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Konfusionsmatrix')
    plt.ylabel('Tatsächliche Werte')
    plt.xlabel('Vorhergesagte Werte')

    # Speichern des Plots als Bild
    plt.savefig(os.path.join(Config.PATH_RF, scaler + 'Scaler/Testdaten/confusion_matrix_Testdatensatz_' +
                             str(testdatensatz) + '_SampleLength_' + str(sample_length) + '_nEstimator_' + str(
        n_estimators) + '.png'))

    # plt.show()

    # txt Datei mit Model Summary speichern
    txt_file_path = os.path.join(Config.PATH_RF, scaler + 'Scaler/Testdaten/model_summary_Testdatensatz_' + str(
        testdatensatz) + '_SampleLength_' + str(sample_length) + '_nEstimator_' + str(n_estimators) + '.txt')

    # Öffnen der Datei im Schreibmodus ('w' für Schreiben)
    with open(txt_file_path, 'w') as file:
        file.write('\n')
        file.write('_________________________________________________________________\n')
        # Hyperparameter
        file.write('Testgenauigkeit: {}\n'.format(accuracy))
        file.write('--------\n')
        file.write("Classification Report:\n {}\n".format(report))
        file.write('_________________________________________________________________\n')

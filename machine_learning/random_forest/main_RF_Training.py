from machine_learning.random_forest.functions_rf import *
from machine_learning.functions_datapreprocessing import scaleData

# ----
# MAIN: TRAINING EINES RANDOM FORESTS
# ----


##############################################################
# EINGABEN:

# Name der Trainingsdatei
data_training = r'output_raw+aug+aug_new2_18600.parquet'

# MinMax, Standard oder No
scaler = 'MinMax'

# Feature Type
feature_type = 'MA_Karle'

# Hyperparameter für RF
sample_lengths = [25, 50, 100, 200, 300, 1860, 9300, 18600]
n_estimators = [10, 100]

##############################################################


print('---- Start Training RF: ----')
print('Rohdatei: ' + data_training)
print(f'Sample Lengths: {sample_lengths}, n_estimators: {n_estimators}')
# Erstellen eines neuen Ordners als Speicherort der Ergebnisse
ordnername = 'RF__' + data_training
output_dir = os.path.join(Config.PATH_RF, ordnername)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print('---------------------')
# Einlesen der Daten
path = os.path.join(Config.PATH_Trainingsdaten, data_training)
data = pd.read_parquet(path)
# Skalierung der Daten:
if scaler == 'MinMax' or scaler == 'Standard':
    data = scaleData(raw_data=data, scaler_type=scaler)
    print('Skalierung: ' + scaler)
elif scaler == 'No':
    print('Keine Skalierung.')
else:
    print('Fehler bei der Auswahl des Scalers.')
print('---------------------')

# Hauptfunktion
trainRF_GridSearch(data_raw=data, n_estimators=n_estimators, sample_lengths=sample_lengths, feature_type=feature_type,
                   scaler=scaler, output_dir=output_dir)

print('---- Ende. ----')

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt


def useTP(csv_file_path, label):
    # Einlesen der CSV-Datei
    df = pd.read_csv(csv_file_path)
    # Filterparameter
    cutoff_frequency = 2.0  # Grenzfrequenz des Filters in Hz
    sampling_rate = 1 / (df['time_[s]'].diff().median())  # Sampling-Rate bestimmen aus Median der Zeitdifferenzen
    nyquist_frequency = 0.5 * sampling_rate
    order = 2  # Ordnung des Filters

    # Butterworth Tiefpassfilter
    normal_cutoff_frequency = cutoff_frequency / nyquist_frequency
    b, a = butter(order, normal_cutoff_frequency, btype='low', analog=False)
    df['filtered_current_mA'] = filtfilt(b, a, df['current_[mA]'])

    # Plotten der originalen und gefilterten Daten
    plt.figure(figsize=(12, 6))
    plt.plot(df['time_[s]'], df['current_[mA]'], label='original', alpha=0.3, color='black')
    plt.plot(df['time_[s]'], df['filtered_current_mA'], label='filtered', linewidth=2, color='r')
    plt.title('Current: ' + label, loc='left')
    plt.xlabel('Time [s]')
    plt.ylabel('Current [mA]')
    plt.legend()
    plt.grid(True)
    plt.show()

# Dateiname der CSV-Dateien
# Testdatensatz 1
path_zahnraeder = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Testdatensatz_1\#_servo_zahnräder\2024-01-29_10-34-59\current.csv"
path_zahnriemen = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Testdatensatz_1\#_servo_zahnriemen\2024-01-29_09-27-56\current.csv"
# Trainingsdaten
path_zahnraeder_training = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Training\#_servo_zahnräder\2023-12-12_12-50-48\current.csv"
path_zahnriemen_training = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Training\#_servo_zahnriemen\2023-12-12_10-16-08\current.csv"


#useTP(path_zahnraeder, 'Servo_Zahnraeder')
#useTP(path_zahnriemen, 'Servo_Zahnriemen')


###########################################################################################################################

def TPonparquet(file_path):
    # Einlesen der CSV-Datei
    df = pd.read_parquet(file_path)
    # Filterparameter
    cutoff_frequency = 2.0  # Grenzfrequenz des Filters in Hz
    sampling_rate = 1 / (df['time_[s]'].diff().median())  # Sampling-Rate bestimmen aus Median der Zeitdifferenzen
    nyquist_frequency = 0.5 * sampling_rate
    order = 2  # Ordnung des Filters

    # Butterworth Tiefpassfilter
    normal_cutoff_frequency = cutoff_frequency / nyquist_frequency
    b, a = butter(order, normal_cutoff_frequency, btype='low', analog=False)
    df['current_[mA]'] = filtfilt(b, a, df['current_[mA]'])

    return df

file_path_raw = r"/raw_data_sorted/#machine_learning/Testdaten/output_Testdatensatz_2_raw.parquet"

df_new = TPonparquet(file_path_raw)

print(df_new)

file_path_save = r"/raw_data_sorted/#machine_learning/Testdaten/output_Testdatensatz_2_filtered.parquet"

df_new.to_parquet(file_path_save)





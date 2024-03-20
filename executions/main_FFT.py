import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.fft import fft, fftfreq


def process_and_plot_fft(file_path, label):
    # Einlesen der CSV-Datei
    df = pd.read_csv(file_path)

    # Extrahieren der Zeit- und Stromdaten aus der DataFrame
    time = df['time_[s]'].to_numpy()
    current = df['current_[mA]'].to_numpy()

    # Interpolation für gleichmäßige Abtastung
    interp_func = interp1d(time, current)
    time_uniform = np.linspace(time.min(), time.max(), len(time))
    current_uniform = interp_func(time_uniform)

    # FFT
    fft_result = fft(current_uniform)
    freqs = fftfreq(len(current_uniform), time_uniform[1] - time_uniform[0])

    # Entferne negative Frequenzen für die Darstellung
    mask = freqs > 0
    fft_result = fft_result[mask]
    freqs = freqs[mask]

    # Logarithmische Darstellung der Amplitude
    plt.loglog(freqs, np.abs(fft_result), label=label)  # Beide Achsen logarithmisch


# Dateiname der CSV-Dateien
# Testdatensatz 1
path_zahnraeder = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Testdatensatz_1\#_servo_zahnräder\2024-01-29_10-34-59\current.csv"
path_zahnriemen = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Testdatensatz_1\#_servo_zahnriemen\2024-01-29_09-27-56\current.csv"
# Trainingsdaten
path_zahnraeder_training = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Training\#_servo_zahnräder\2023-12-12_12-50-48\current.csv"
path_zahnriemen_training = r"C:\Users\maxi1\Documents\UNI MASTER KIT\#MASTERARBEIT\05 Sonstige Dokumente\Data\#Training\#_servo_zahnriemen\2023-12-12_10-16-08\current.csv"


# Plot vorbereiten
plt.figure(figsize=(10, 6))

# Daten verarbeiten und plotten
process_and_plot_fft(path_zahnriemen_training, 'Servo_Zahnriemen')
process_and_plot_fft(path_zahnraeder_training, 'Servo_Zahnraeder')

# Plot finalisieren
plt.title('Logarithmische Darstellung der FFTs')
plt.xlabel('Frequenz [Hz]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True, which="both", ls="-")
plt.show()

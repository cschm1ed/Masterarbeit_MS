import pandas as pd
from datetime import datetime
import functions_decodedata
import matplotlib.pyplot as plt
import os

verzeichnis_pfad = 'raw_data_sorted/'  # Passe den Pfad zu deinem Verzeichnis an

ordner_liste = next(os.walk(verzeichnis_pfad))[1]

print(ordner_liste)

zu_überspringender_ordner = '#alt'  # Ersetze dies durch den Namen des Ordners, den du überspringen möchtest
for ordner in ordner_liste:
    if ordner != zu_überspringender_ordner:
        dateiname = 'raw_data_sorted/' + ordner + '/i2c_export.csv'
        print(dateiname)

        try:
            result = functions_decodedata.decodeCurrent(dateiname)
            print(result)
            # Liniendiagramm (Line Plot)
            plt.plot(result['time[s]'], result['current[mA]'], marker='None', linestyle='-', color='b')  # 'o' für Marker, '-' für Linienstil, 'b' für die Farbe blau
            plt.xlabel('time[s]')
            plt.ylabel('current[mA]')
            plt.title('Test_' + dateiname)
            plt.grid(True)
            plt.show()
        except Exception as e:
            print(f"Fehler beim Verarbeiten des Ordners '{ordner}': {e}")
            continue  # Springe zum nächsten Ordner, auch wenn ein Fehler auftritt


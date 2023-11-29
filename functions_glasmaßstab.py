import pandas as pd

# Dateipfad zur CSV-Datei
dateiname = 'raw_data_sorted/test_LogicAnalyzer/Glasmaßstab/Richtung Modell_Stecker/digital_20cm_mitPausen.csv'

# Einlesen in ein Pandas dataframe
df = pd.read_csv(dateiname)


# Sequenzen zu überprüfen (für Bewegung in Richtung des Steckers)
# Sequenzen zu überprüfen (für Bewegung in Richtung des Steckers/ Modell)
sequence1 = [(1, 0), (1, 1), (0, 1), (1, 1), (0, 1), (1, 1), (0, 1), (0, 0), (0, 1), (0, 0), (0, 1), (0, 0)]
sequence2 = [(1, 0), (1, 1), (0, 1), (1, 1), (1, 1), (0, 1), (1, 1), (0, 1), (0, 0), (0, 1), (0, 0), (0, 1), (0, 0)]
sequence3 = [(1,0),(1,1),(0,1),(1,1),(1,1),(0,1),(1,1),(0,1),(0,0),(0,1),(1,1),(0,0),(0,1),(0,0)]
sequence4 = [(1,0),(1,1),(0,1),(1,1),(1,1),(0,1),(1,1),(0,1),(1,0),(0,0),(0,1),(1,1),(0,0),(0,1),(0,0)]
sequence5 = [(1,0),(1,1),(0,1),(1,1),(0,1),(1,1),(0,1)]
sequence6 = [(1,0),(1,1),(0,1),(1,1),(1,1),(0,1),(1,1),(0,1),(0,0),(0,1),(1,1),(1,0),(0,1),(0,0)]
sequence =[(1,0),(0,0),(1,0),(0,0),(1,0),(0,0),(0,1),(1,1)]
# Funktion: Check durchführen
def suche_sequenz(df, *sequences):
    positionszähler = 0
    counter = 0
    gesamt = []
    takt = 1.517  # Annahme eines Standardwerts für 'takt'

    for i in range(len(df)-15):
        for idx, sequence_to_check in enumerate(sequences, start=1):
            subset = df.iloc[i:i + len(sequence_to_check)]
            if (subset[['Channel 4', 'Channel 5']].values == sequence_to_check).all():
                print(f"Sequenz {idx} gefunden ab Zeile {i}")
                counter += 1
                gesamt.append(i)
                i += len(sequence_to_check) - 1  # Gehe zur nächsten möglichen Sequenz
                positionszähler += takt * (11 + idx)
                break
            else:
                continue
            break

    return counter, gesamt, positionszähler

counter, gesamt, position = suche_sequenz(df, sequence1, sequence2, sequence3, sequence4, sequence5, sequence6, sequence_test)

print("Anzahl der gefundenen Sequenzen:", counter)
print("Positionen der gefundenen Sequenzen:", gesamt)
print("Aktuelle Position des Schiebers:", position/10000 , " cm")


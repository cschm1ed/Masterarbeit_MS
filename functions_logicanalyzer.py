import pandas as pd

# Funktionen zu Berechnung zwischen hex, bin, dez:

# Funktion zum Entschlüsseln des Zweierkomplements
def decode_twos_complement(binary_string):
    is_negative = binary_string[0] == '1'
    if is_negative:
        inverted = ''.join(['1' if bit == '0' else '0' for bit in binary_string])
        inverted = bin(int(inverted, 2) + 1)[2:]
    decimal_value = int(inverted if is_negative else binary_string, 2)
    return -decimal_value if is_negative else decimal_value

# Funktion zum Umwandeln von Binär in Dezimal
def bin_to_decimal(bin_string):
    return int(bin_string, 2)

# Funktion zum Umwandeln von Hex in Binär
def hex_to_bin(hex_string):
    if isinstance(hex_string, str):
        return bin(int(hex_string, 16))[2:]
    else:
        # Behandeln Sie den Fall, in dem hex_string keine Zeichenfolge ist.
        # Sie können eine Ausnahme auslösen, eine Fehlermeldung ausgeben oder dies nach Bedarf behandeln.
        return None  # Oder eine Ausnahme auslösen oder den Fehler auf geeignete Weise behandeln

# Funktion zum Einlesen + dekodieren der Stromstärke aus dem Logic 2 Export (digital_table.csv):
def getcurrent(csv_datei):

    # Dateipfad zur CSV-Datei
    dateiname = 'raw_data_sorted/test_LogicAnalyzer/' + csv_datei + '.csv'

    # Einlesen in ein Pandas dataframe
    df = pd.read_csv(dateiname)

    # Bedingung überprüfen, ob 'data' die Werte '0x04' (unabhängig von der Groß- und Kleinschreibung) enthält (stellt die Read Bedingung dar)
    bedingung = df['data'].str.contains(r'0x04', na=False, case=False, regex=True) #& df['ack'] == True

    # Den Index der Zeile mit der erfüllten Bedingung (True) erhalten
    index_zeile = df.index[bedingung]

    # Prüfung der nächsten Zeilen
    next_index = index_zeile + 3
    new_bedingung = df['type'].eq('data').loc[next_index]

    if new_bedingung.all():
        # Index der wirklichen Daten berechnen und zusammenfügen
        index1 = index_zeile + 3
        index2 = index_zeile + 4
        merged_index = index1.union(index2)
    else:
        false_indexes = new_bedingung.index[new_bedingung == False]
        false_indexes_neu = false_indexes-3
        index_corect = index_zeile.difference(false_indexes_neu)
        index1 = index_corect + 3
        index2 = index_corect + 4
        merged_index = index1.union(index2)

    # Daten Zeilen zusammenfügen
    data_zeilen = df.loc[merged_index]

    # Umrechnung von hex in bin und hinzufügen von 0en
    data_zeilen['data_bin_old'] = data_zeilen['data'].apply(hex_to_bin)
    data_zeilen['data_bin'] = data_zeilen['data_bin_old'].str.replace(' ', '').str.zfill(8)

    # Saplten 'start_time' und 'data_bin_neu' extrahieren
    data_new = data_zeilen[['start_time','data_bin']]

    # Indexreset
    data_new.reset_index(drop=True, inplace=True)

    # Länge von data_new berechnen
    anzahl_data_new = len(data_new)

    # Ergebnis DataFrame mit den Spalten 'time[s]' und 'data_bin' erstellen (noch komplett leer)
    ergebnis_df = pd.DataFrame(columns=['time[s]', 'data_bin'])

    # Für Errors:
    #print(data_new)
    #data_new.to_csv('errors/vergleichlogicarduino.txt', sep=',', index=False)

    # for-Schleife zum Hinzufügen von Daten
    for i in range(0,anzahl_data_new-1,2):
        # Timestamp wird von ersten Datenpaket genommen
        time = data_new.loc[i, 'start_time']
        # Auslesen des ersten Register-Datenpakets
        paket1 = data_new.loc[i,'data_bin']
        # Auslesen des zweiten Register-Datenpakets
        paket2 = data_new.loc[i+1,'data_bin']
        # Zusammenfügen beider Register-Datenpakete
        data = paket1 + paket2
        # Hinzufügen zum ergebnis_df
        ergebnis_df.loc[i] = [time,data]

    # Umrechnung von bin in dez (auch das Zweierkomplement für negative Zahlen wird beachtet)
    ergebnis_df['data_dez'] = ergebnis_df['data_bin'].apply(decode_twos_complement)

    # Wert für current_LSB (in Adafruit_INA219 Bibliothek zu finden)
    current_LSB = 1e-4

    # Berechnung von current in A und mA
    ergebnis_df['current[A]'] = ergebnis_df['data_dez'] * current_LSB
    ergebnis_df['current[mA]'] = ergebnis_df['current[A]'] * 1000

    # Ausgabe des ergebnis_df
    #print(ergebnis_df)

    #Rückgabe des ergebnis_df
    return ergebnis_df


import pandas as pd
from saleae import automation
import os
import os.path
import subprocess
from datetime import datetime
from saleae.automation import RadixType
from saleae.automation import DataTableExportConfiguration


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
def getcurrent(dateipfad):

    # Dateipfad zur CSV-Datei
    #dateiname = 'raw_data_sorted/test_LogicAnalyzer/' + csv_datei + '.csv'

    # Einlesen in ein Pandas dataframe
    df = pd.read_csv(dateipfad)

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


# Funktionen zum Steuern von Logic 2:
# Code noch weiter anpassen (damit Trigger funktioniert + Endzeit festgelegt werden kann in Funktionsaufruf + Speicherort der cs Datei zurückgegeben wird)
def startlogic2(time):
    # https://saleae.github.io/logic2-automation/

    # Öffnet Logic 2 Anwendung
    exe_datei_pfad = 'C:\Program Files\Logic\Logic.exe'
    prozess = subprocess.Popen([exe_datei_pfad])

    with automation.Manager.connect(port=10430) as manager:
        device_configuration = automation.LogicDeviceConfiguration(
            enabled_digital_channels=[0, 1, 2, 3],
            digital_sample_rate=50_000_000,
            # digital_threshold_volts=3.3,
        )

        # Record 5 seconds of data before stopping the capture
        capture_configuration_timecapture = automation.CaptureConfiguration(
            capture_mode=automation.TimedCaptureMode(duration_seconds=time)
        )

        # Record 60 seconds of data after trigger of channel 3
        triggertype = automation.DigitalTriggerType.RISING
        capture_configuration_trigger = automation.CaptureConfiguration(
            capture_mode=automation.DigitalTriggerCaptureMode(trigger_channel_index=3, trigger_type=triggertype, trim_data_seconds=2, after_trigger_seconds=time)
        )

        with manager.start_capture(
                #device_id='A60D1D2452ABF025',
                device_id='F4241', # für Demo Version
                device_configuration=device_configuration,
                capture_configuration=capture_configuration_trigger) as capture:
            # Wait until the capture has finished
            # This will take about 5 seconds because we are using a timed capture mode
            capture.wait()

            # Add an analyzer to the capture
            i2c_analyzer = capture.add_analyzer('I2C', label=f'I2C', settings={
                'SDA': 1,
                'SCL': 0
            })

            # Ordner erstellen (in welchem die Daten gespeichert werden
            ordnername = (
                "C:\\Users\\maxi1\\Documents\\UNI MASTER KIT\\#MASTERARBEIT\\05 Sonstige Dokumente\\PycharmProjects\\Masterarbeit_Schubert\\raw_data_sorted\\test_LogicAnalyzer")
            output_dir = os.path.join(ordnername, f'digital_output-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
            os.makedirs(output_dir)

            # Konfiguration von export Analyzer
            radixtype = RadixType.HEXADECIMAL
            config_export_analyzer = DataTableExportConfiguration(analyzer=i2c_analyzer, radix=radixtype)
            # Export von I2C Analyzer Daten
            analyzer_export_filepath = os.path.join(output_dir, 'i2c_export.csv')
            capture.export_data_table(
                filepath=analyzer_export_filepath,
                analyzers=[i2c_analyzer, config_export_analyzer]
            )


            # Export von raw digital data
            # capture.export_raw_data_csv(directory=output_dir, digital_channels=[0, 1, 2])

            # Speichern der capture Datei
            capture_filepath = os.path.join(output_dir, 'capture.sal')
            capture.save_capture(filepath=capture_filepath)

        speicherort_csv_file = output_dir + '\i2c_export.csv'
    return speicherort_csv_file


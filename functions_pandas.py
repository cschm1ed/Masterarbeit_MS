import pandas as pd
import os


# Einlesen der txt-Dateien in pandas dataframes
def savetxtaspandas():
    # Liste für DataFrames erstellen
    dataframes_list = []

    # Ordnername:
    ordnername = "raw_data_unsorted"
    # todo: noch so anpassen, dass der Ordner raw_data_sorted genutzt wird

    # Durch alle Dateien im Ordner iterieren
    for index, dateiname in enumerate(os.listdir(ordnername)):
        if dateiname.endswith(".txt"):  # Prüfen, ob es sich um eine Textdatei handelt
            dateipfad = os.path.join(ordnername, dateiname)

            try:
                # Einlesen der TXT-Datei mit read_table
                data = pd.read_table(dateipfad, delim_whitespace=True)

                # Neue Spaltennamen zuweisen
                #new_columns = ['Stromstärke [mA]', 'Position [dauer]', 'Timestampf [ms]']
                #data.columns = new_columns

                # Das Datenframe zur Liste hinzufügen
                dataframes_list.append(data)


            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei: {dateipfad}")
                continue  # Zur nächsten Datei springen


    # print(dataframes_list)
    rückgabe = dataframes_list

    return rückgabe

# Hier wird die Zeitspalte neu angepasst
def updatetimestamp(dataframes_list):
    # Timestamp Spalte verrechnen
    for i, df in enumerate(dataframes_list):
        df['Time[s]'] = df['Timestamp[ms]']/1000

    #print(dataframes_list)


# Hier werden alle dataframes auf die selbe Länge gebracht
def getsamelength(dataframes_list):
    # Die DataFrames in dataframes_list auf die gleiche Länge bringen
    max_laenge = max(len(df) for df in dataframes_list)

    for i, df in enumerate(dataframes_list):
        if len(df) < max_laenge:
            # Fehlende Zeilen mit NaN-Werten auffüllen
            fehlende_zeilen = max_laenge - len(df)
            dataframes_list[i] = pd.concat(
                [df, pd.DataFrame([pd.Series([None] * len(df.columns)) for _ in range(fehlende_zeilen)])],
                ignore_index=True)



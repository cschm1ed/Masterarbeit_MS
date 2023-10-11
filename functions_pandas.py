import pandas as pd
import os


# Einlesen der txt-Dateien in pandas dataframes
def savetxtaspandas(ordner):
    # Liste für dataframes erstellen
    dataframes_list = []
    # Ordnername:
    ordnername = 'raw_data_sorted/' + ordner
    # Durch alle Dateien im Ordner iterieren
    for index, dateiname in enumerate(os.listdir(ordnername)):
        if dateiname.endswith(".txt"):  # Prüfen, ob es sich um eine Textdatei handelt
            dateipfad = os.path.join(ordnername, dateiname)
            try:
                # Einlesen der TXT-Datei mit read_table
                data = pd.read_table(dateipfad, delim_whitespace=True)
                # Das Datenframe zur Liste hinzufügen
                dataframes_list.append(data)
            except Exception:
                print(f"Fehler beim Verarbeiten der Datei: {dateipfad}")
                continue  # Zur nächsten Datei springen
    # print(dataframes_list)
    # es wird die Liste aller dataframes zurückgegeben:
    return dataframes_list


# Hier wird die Zeitspalte neu angepasst
def updatetimestamp(dataframes_list):
    updated_dataframes = []
    # Timestamp Spalte verrechnen
    for i, df in enumerate(dataframes_list):
        df['Time[s]'] = df['Timestamp[ms]']/1000
        updated_dataframes.append(df)
    return updated_dataframes


# Umrechnung von Position[dauer] in Position[mm]:
def getcorrectposition(dataframes_list,filter):
    updated_dataframes = []
    # hier wird der Nullpunkt festgelegt; dabei gibt es einen Unterschied zwischen mit/ohne Filter
    # die Werte müssen noch manuell eingetragen werden, sollten aber später immer gleich sein (bei der Verwendung des endgültigen Sensors)
    Nullpunkt_mitFilter = 618
    Nullpunkt_ohneFilter = 648
    if filter == True:
        Nullpunkt = Nullpunkt_mitFilter
    else:
        Nullpunkt = Nullpunkt_ohneFilter
    # Position[dauer] Spalte verrechnen
    for i, df in enumerate(dataframes_list):
        df['Position[cm]'] = ((df['Position[dauer]']-Nullpunkt)/2) * 0.03432
        updated_dataframes.append(df)
    return updated_dataframes


# Umrechnung von Strom[bit] in Strom[mA]:
def getcorrectcurrent(dataframes_list):
    updated_dataframes = []
    # hier wird der Nullpunkt festgelegt; dabei gibt es einen Unterschied zwischen mit/ohne Filter
    # die Werte müssen noch manuell eingetragen werden, sollten aber später immer gleich sein
    offset = 2500    #Spannung in mV bei dem keine Stromstärke vorhanden ist; muss nochmals gemessen werden
    sensitivity = 185   #Sensitivtät des Sensore; bei 5A Version sind das 185mV
    # Strom[bit] Spalte verrechnen
    for i, df in enumerate(dataframes_list):
        spaltenname = 'Strom[bit]'
        if spaltenname in df.columns:
            df['Strom[mV]'] = (df['Strom[bit]'] / 1024) * 5000
            df['Strom[A]'] = (df['Strom[mV]'] - offset) / sensitivity
            df['Strom[mA]'] = df['Strom[A]'] * 1000
            updated_dataframes.append(df)
            #print('vorhanden')
        else:
            updated_dataframes.append(df)
            #print('nicht vorhanden')
    return updated_dataframes


# Überprüfen der richtigen Spaltennamen; bzw. korrigieren damit alle Spaltennamen stimmen:
def checkcolumnnames(dataframes_list):
    updated_dataframes = []
    for df in dataframes_list:
        spalte_2 = df.columns[1]
        if spalte_2 == 'Position[dauer]':
            updated_dataframes.append(df)
        else:
            for index, row in df.iterrows():
                wert = row.iloc[1]  # Zugriff auf den Wert in der zweiten Spalte (Index 1)
                if wert == 'Position[dauer]':
                    #print(f"Zeile {index}, Wert: {wert}")
                    neuer_spaltennamen = df.iloc[index]
                    df = df.rename(columns=neuer_spaltennamen)
                    df = df.drop(df.index[0:index+1])
                    df = df.reset_index(drop=True)
                    #print(df)
                    break
            updated_dataframes.append(df)
    return updated_dataframes


# Entfernen der nicht gebrauchten Spalten:
def deletenotneededcolums(dataframes_list):
    updated_dataframes = []
    # Liste der zu löschenden Spalten
    zu_loeschende_spalten = ['Strom[bit]', 'Position[dauer]', 'Strom[A]', 'Strom[mV]', 'Timestamp[ms]']
    for df in dataframes_list:
        for spaltenname in zu_loeschende_spalten:
            if spaltenname in df.columns:
                # Die Spalte ist im DataFrame vorhanden, also löschen Sie sie
                df.drop(spaltenname, axis=1, inplace=True)
        updated_dataframes.append(df)

    return updated_dataframes



# GESAMTFUNKTION
# Hier werden alle Funktionen aufgerufen um die Daten so verarbeitet zu haben, damit sie für die matplotlib und plotly Funktionen genutzt werden können
# der übergegebene Ordner muss sich in dem Ordner "raw_data_sorted" befinden
def doallpandasfunction(ordner,filter):
    # 1.: txt-Daten werden in pandas dataframes Listen gespeichert
    dataframes_list = savetxtaspandas(ordner=ordner)
    # 2.: Überprüfen ob Zeile "Strom[mA],Position[dauer],Timestamp[ms]" als Spaltennamen genommen wurde; falls nicht wird dies korrigiert
    dataframes_list_correctrows = checkcolumnnames(dataframes_list=dataframes_list)
    # 3.: Nun wird die Spalte 'Time[s]' hinzugefügt
    dataframes_list_correctrows_correcttime = updatetimestamp(dataframes_list=dataframes_list_correctrows)
    # 4.: Nun wird die Spalte 'Position[cm]' hinzugefügt
    dataframes_list_correctrows_correcttime_correctposition = getcorrectposition(dataframes_list=dataframes_list_correctrows_correcttime,filter=filter)
    # 5.: Nun wird die Spalte 'Strom[bit]' in 'Strom[mA]' umgewandelt
    dataframes_list_correctrows_correcttime_correctposition_correctcurrent = getcorrectcurrent(dataframes_list=dataframes_list_correctrows_correcttime_correctposition)
    # 6.: Nun werden die nicht gebrauchten Spalten gelöscht, sodass nur noch folgenden Spalten vorhanden sind:
    #   'Strom[mA]'  'Position[cm]'  'Time[s]
    dataframes_list_correctrows_correcttime_correctposition_correctcurrent_correctcolumns = deletenotneededcolums(dataframes_list_correctrows_correcttime_correctposition_correctcurrent)
    # Nochmals in einfachem Namen speichern:
    dataframes_list_correct = dataframes_list_correctrows_correcttime_correctposition_correctcurrent_correctcolumns

    # Rückgabe der verarbeiteten dataframes Liste
    return dataframes_list_correct





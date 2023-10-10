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

                # Neue Spaltennamen zuweisen
                #new_columns = ['Stromstärke [mA]', 'Position [dauer]', 'Timestampf [ms]']
                #data.columns = new_columns

                # Das Datenframe zur Liste hinzufügen
                dataframes_list.append(data)


            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei: {dateipfad}")
                continue  # Zur nächsten Datei springen


    # print(dataframes_list)

    # es wird die Liste aller dataframes zurückgegeben:
    return dataframes_list

# Hier wird die Zeitspalte neu angepasst
def updatetimestamp(dataframes_list):
    try:
        # Timestamp Spalte verrechnen
        for i, df in enumerate(dataframes_list):
            df['Time[s]'] = df['Timestamp[ms]']/1000
        print(f'        Spalte \'Time[s]\' wurde der dataframes-Liste erfolgreich hinzugefügt.')
    except KeyError:
        # Wenn die 'Timestamp[ms]'-Spalte nicht in einem DataFrame vorhanden ist
        print(f'        Error: Spalte \'Timestamp[ms]\' wurde nicht gefunden (Position: {i+1})')
    except Exception:
        # Für andere unerwartete Fehler
        print(f'        Error: Unerwarteter Fehler aufgetreten (Position: {i+1})')
    #print(dataframes_list)





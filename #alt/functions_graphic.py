# ----
# FUNKTIONEN ZUR GRAPHISCHEN VERANSCHAULICHUNG
# ----

import os
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt


# Funktion zur Erstellung der plotly Figures (für Position + Stromstärke)
def createPlotlyFigures():
    ordner_liste = [d for d in os.listdir('../raw_data_sorted/#fertig') if
                    os.path.isdir(os.path.join('../raw_data_sorted/#fertig\\', d))]

    for ordner in ordner_liste:
        verzeichnis = 'raw_data_sorted\\#fertig\\' + ordner

        # Zugriff auf Daten der Messung
        with open(verzeichnis + '\\used_parts.txt', 'r') as file:
            lines = file.readlines()
            txt_name_motor_list = lines[2].split(' ',1)
            txt_name_getriebe_list = lines[3].split(' ',1)
            txt_time = lines[6]

            txt_name_motor = txt_name_motor_list[1]
            txt_name_getriebe = txt_name_getriebe_list[1]

        print('--- ' + verzeichnis + ':')

        verzeichnis_position = os.path.join(verzeichnis, 'position.csv')
        df_position = pd.read_csv(verzeichnis_position)
        # Linienplot erstellen
        fig_position = px.line(df_position, x='time_[s]', y='position_[mm]', title='Position: (' + txt_name_motor + '_' + txt_name_getriebe + '__' + txt_time + ')')
        fig_position.show()

        verzeichnis_current = os.path.join(verzeichnis, 'current.csv')
        df_current = pd.read_csv(verzeichnis_current)
        # Linienplot erstellen
        fig_current = px.line(df_current, x='time_[s]', y='current_[mA]', title='Current: (' + txt_name_motor + '_' + txt_name_getriebe + '__' + txt_time + ')')
        fig_current.show()

        print('\t.... Figures erfolgreich erstellt.')

    print('--- Für alle Ordner in "raw_data_sorted" wurden Figures erstellt.')

# Funktion zur Erstellung der matplotlib Figures (für Position + Stromstärke) & automatisches speichern
def createandsaveMatplotlibFigures():
    ordner_liste = [d for d in os.listdir('../raw_data_sorted/#fertig') if
                    os.path.isdir(os.path.join('../raw_data_sorted/#fertig\\', d))]

    for ordner in ordner_liste:
        verzeichnis = 'raw_data_sorted\\#fertig\\' + ordner

        # Zugriff auf Daten der Messung
        with open(verzeichnis + '\\used_parts.txt', 'r') as file:
            lines = file.readlines()
            txt_name_motor_list = lines[2].split(' ', 1)
            txt_name_getriebe_list = lines[3].split(' ', 1)
            txt_time = lines[6]

            txt_name_motor = txt_name_motor_list[1]
            txt_name_getriebe = txt_name_getriebe_list[1]

        print('--- ' + verzeichnis + ':')

        dateinamen = ['current_diagramm.png', 'position_diagramm.png']
        alle_vorhanden = True
        for dateiname in dateinamen:
            pfad_zur_datei = os.path.join(verzeichnis, dateiname)
            if not os.path.isfile(pfad_zur_datei):
                alle_vorhanden = False
                break

        if alle_vorhanden == False:
            # Diagramm für Positionsverlauf erstellen
            verzeichnis_position = os.path.join(verzeichnis, 'position.csv')
            df_position = pd.read_csv(verzeichnis_position)
            # Linienplot erstellen
            x_position = df_position['time_[s]']
            y_position = df_position['position_[mm]']
            plt.figure(figsize=(10, 8))
            plt.plot(x_position, y_position, linestyle='-', color='blue', label=txt_name_motor + txt_name_getriebe)
            plt.title('Position:', loc='left')
            plt.title(txt_time, loc='right')
            plt.xlabel('Zeit [s]')
            plt.ylabel('Position [mm]')
            plt.grid(True)
            plt.legend()
            plt.savefig(verzeichnis + '\\position_diagramm.png')
            #plt.show()


            # Diagramm für Stromstärkenverlauf erstellen
            verzeichnis_current = os.path.join(verzeichnis, 'current.csv')
            df_current = pd.read_csv(verzeichnis_current)
            # Linienplot erstellen
            x_current = df_current['time_[s]']
            y_current = df_current['current_[mA]']
            plt.figure(figsize=(10, 8))
            plt.plot(x_current, y_current, linestyle='-', color='red', label=txt_name_motor + txt_name_getriebe)
            plt.title('Current:', loc='left')
            plt.title(txt_time, loc='right')
            plt.xlabel('Zeit [s]')
            plt.ylabel('Current [mA]')
            plt.grid(True)
            plt.legend()
            plt.savefig(verzeichnis + '\\current_diagramm.png')
            #plt.show()

            print('\t.... Figures erfolgreich gespeichert.')
        else:
            print('\t.... Figures bereits vorhanden.')

    print('--- Für alle Ordner in "raw_data_sorted" wurden die Figures erfolgreich gespeichert.')
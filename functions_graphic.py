import os
import plotly.express as px
import pandas as pd


def createPlotlyFigures():
    ordner_liste = [d for d in os.listdir("raw_data_sorted") if
                    os.path.isdir(os.path.join("raw_data_sorted", d)) and "digital_output" in d]

    for ordner in ordner_liste:
        verzeichnis = 'raw_data_sorted\\' + ordner

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
        fig_position = px.line(df_position, x='time_[s]', y='position_[mm]', title='Positionsverlauf: (' + txt_name_motor + '_' + txt_name_getriebe + '__' + txt_time + ')')
        fig_position.show()

        verzeichnis_current = os.path.join(verzeichnis, 'current.csv')
        df_current = pd.read_csv(verzeichnis_current)
        # Linienplot erstellen
        fig_current = px.line(df_current, x='time_[s]', y='current_[mA]', title='Stromstärkensverlauf: (' + txt_name_motor + '_' + txt_name_getriebe + '__' + txt_time + ')')
        fig_current.show()

        print('\tFigures erfolgreich erstellt.')


createPlotlyFigures()
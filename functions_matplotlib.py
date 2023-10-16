import matplotlib.pyplot as plt

# Hier kann entweder ein Liniendiagramm erzeugt werden (entweder Position[dauer] oder Strom[mA]
def savelineplot(y_axes,dataframes_list,title):
    # Liniendiagramme für jede DataFrame in der Liste erstellen und anzeigen
    for i, df in enumerate(dataframes_list):
        # Größe des Diagramms festlegen
        plt.figure(figsize=(8, 6))

        # Erstellen des Diagramms
        plt.plot(df['Time[s]'],df[y_axes], marker='None', linestyle='-', color='b', label=title)
        plt.plot()

        plt.title(title)
        plt.xlabel('Zeit [s]')
        plt.ylabel(y_axes)
        plt.legend()

        # Hinzufügen von Gitterlinien
        plt.grid(True)

        # Diagramm speichern
        speicherort_dateiname = 'figures\\linechart_' + title + '_' + str(i+1) + '.png'
        plt.savefig(speicherort_dateiname)

        print('Die figures wurden erfolgreich erstellt.')


# Hier können zwei verschiedene Dataframes verglichen werden
def comparelineplot(y_axes,dataframe_servo,dataframe_schritt,title):
    # Größe des Diagramms festlegen
    plt.figure(figsize=(8, 6))

    # Erstellen des Diagramms
    plt.plot(dataframe_servo['Time[s]'], dataframe_servo[y_axes], marker='None', linestyle='-', color='b', label='Servomotor')
    plt.plot(dataframe_schritt['Time[s]'], dataframe_schritt[y_axes], marker='None', linestyle='-', color='r', label='Schrittmotor')
    plt.title(title)
    plt.xlabel('Zeit [s]')
    plt.ylabel(y_axes)
    plt.legend()
    plt.grid(True)

    # Zeigt das Diagramm in einem Fenster an
    #plt.show()

    # Diagramm speichern
    speicherort_dateiname = 'figures\\linechart_' + title + '_' + '.png'
    plt.savefig(speicherort_dateiname)

    print('Die figure wurde erfolgreich erstellt.')
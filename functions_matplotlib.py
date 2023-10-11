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
import functions_logicanalyzer
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#dateiname = 'digital_table_delay(1000)'
#dateiname = 'digital_table_delay(2)'
#dateiname = 'digital_table_delay(2)_115200'
#dateiname = 'digital_table_delay(5)_115200'
dateiname = 'digital_VergleichArduino'
dateiname = 'digital_referencerun1'

ergebnis_df = functions_logicanalyzer.getcurrent(csv_datei=dateiname)

print(ergebnis_df)

# Neuer Speicherort (z.B. auf dem Desktop) und Dateiname festlegen
#dateipfad = r'raw_data_sorted/test_LogicAnalyzer/results/' + dateiname + '.txt'

# DataFrame in eine Textdatei mit einem benutzerdefinierten Trennzeichen (z.B. Tabulator) speichern
#ergebnis_df.to_csv(dateipfad, sep=',', index=False)

# Grafische Veranschaulichung:

# Erstellen Sie ein Liniendiagramm mit den entsprechenden x- und y-Spalten aus dem DataFrame
fig = px.line(ergebnis_df, x='time[s]', y='current[mA]', title=dateiname)
# Hier werden weitere Anpassungen am Diagramm vorgenommen
# Achsentitel hinzufügen
fig.update_xaxes(title_text='Zeit [s]')
fig.update_yaxes(title_text='Strom [mA]')
# Diagrammtitel ändern
#fig.update_layout(title='Angepasstes Scatter-Plot')
# Hinzufügen einer Legende
fig.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
# Farbpalette ändern
#fig.update_traces(marker=dict(color='red'), selector=dict(mode='markers'))
# Diagrammgröße ändern
#fig.update_layout(width=800, height=400)
# Hinzufügen von Gitterlinien
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
# Diagramm anzeigen
fig.show()




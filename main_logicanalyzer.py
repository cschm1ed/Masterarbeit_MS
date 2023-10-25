import functions_logicanalyzer

#dateiname = 'digital_table_delay(1000)'
#dateiname = 'digital_table_delay(2)'
#dateiname = 'digital_table_delay(2)_115200'
#dateiname = 'digital_table_delay(5)_115200'

ergebnis_df = functions_logicanalyzer.getcurrent(csv_datei=dateiname)

print(ergebnis_df)

# Neuer Speicherort (z.B. auf dem Desktop) und Dateiname festlegen
dateipfad = r'raw_data_sorted/test_LogicAnalyzer/results/' + dateiname + '.txt'

# DataFrame in eine Textdatei mit einem benutzerdefinierten Trennzeichen (z.B. Tabulator) speichern
ergebnis_df.to_csv(dateipfad, sep=',', index=False)

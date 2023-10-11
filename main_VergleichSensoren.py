# main_VergleichSensoren:

# hier werden die verschiedenen Sensoren verglichen

# Import der ganzen Funktionen:
import functions_pandas
import functions
import functions_plotly
import functions_matplotlib

# Aktuell: Vergleich der Stromsensoren


# Aufrufen aller Ordnernamen in raw_sorted_data:
ordnernamen = functions.getallfoldernames()
print('Vorhandene Ordner in \'raw_sorted_data\':')
for element in ordnernamen:
    print('     ' + element)

# Nun kann der Ordner aus der Konsole kopiert werden:

# Komplette Verarbeitung der Daten
correct_dataframes_list = functions_pandas.doallpandasfunction(
    ordner='20231004__USS_ACS712_withoutfilter_50Hz_Servo_ZR', filter=False)
# Ausgabe der dataframes Liste
# print(correct_dataframes_list)

# Grafische Verarbeitung der dataframes Liste:

# Plotly Funktionen
#functions_plotly.showlineplot(y_axes='Position[cm]', dataframes_list=correct_dataframes_list, title='test')

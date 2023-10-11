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
correct_dataframes_list_1 = functions_pandas.doallpandasfunction(
    ordner='20231010__USS_ACS712_withfilter_50Hz_Servo_ZR', filter=True)

correct_dataframes_list_2 = functions_pandas.doallpandasfunction(
    ordner='20231004__USS_INA219_withfilter_50Hz_Servo_ZR', filter=False)



# Ausgabe der dataframes Liste
#print(correct_dataframes_list_1)


# Grafische Verarbeitung der dataframes Liste:

# Plotly Funktionen
functions_plotly.showlineplot(y_axes='Strom[mA]', dataframes_list=correct_dataframes_list_1, title='ACS712')
functions_plotly.showlineplot(y_axes='Strom[mA]', dataframes_list=correct_dataframes_list_2, title='INA219')




# test_plotly:
# .py Datei zum Testen von neuen plotly-Funktionen

import functions_pandas
import functions
import functions_plotly

# Aktuell: Vergleich der Stromsensoren

# Aufrufen aller Ordnernamen in raw_sorted_data
# werden in einem Array gespeichert
ordnernamen = functions.getallfoldernames()

# Nun wird durch das Array iteriert und alle Ordnernamen ausgegeben; welche im Ordner 'raw_sorted_data' vorhanden
print('Vorhandene Ordner:')
for element in ordnernamen:
    print(element)

# todo: das Folgende soll automatisiert erfolgen
# Hier werden die dataframes Listen erstellt, dies erfolgt aktuell noch manuell
list_USS_ACS712_withfilter_50Hz_Servo_ZR = functions_pandas.savetxtaspandas(ordner=ordnernamen[1])
list_USS_ACS712_withoutfilter_50Hz_Servo_ZR = functions_pandas.savetxtaspandas(ordner=ordnernamen[2])
list_USS_INA219_withfilter_50Hz_Servo_ZR = functions_pandas.savetxtaspandas(ordner=ordnernamen[3])
list_USS_INA219_withoutfilter_50Hz_Servo_ZR = functions_pandas.savetxtaspandas(ordner=ordnernamen[4])

# Spalte 'Time[ms]' wird hinzugefügt:
print()
print()
print('Hinzufügen der Spalte \'Time[s]\':')
print()
print('dataframes-Liste: ' + ordnernamen[1] + ':')
functions_pandas.updatetimestamp(dataframes_list=list_USS_ACS712_withfilter_50Hz_Servo_ZR)
print('dataframes-Liste: ' + ordnernamen[2] + ':')
functions_pandas.updatetimestamp(dataframes_list=list_USS_ACS712_withoutfilter_50Hz_Servo_ZR)
print('dataframes-Liste: ' + ordnernamen[3] + ':')
functions_pandas.updatetimestamp(dataframes_list=list_USS_INA219_withfilter_50Hz_Servo_ZR)
print('dataframes-Liste: ' + ordnernamen[4] + ':')
functions_pandas.updatetimestamp(dataframes_list=list_USS_INA219_withoutfilter_50Hz_Servo_ZR)


# # Ausgabe der Dataframes Listen:
# print(list_USS_ACS712_withfilter_50Hz_Servo_ZR)
# print(list_USS_ACS712_withoutfilter_50Hz_Servo_ZR)
# print(list_USS_INA219_withfilter_50Hz_Servo_ZR)
# print(list_USS_INA219_withoutfilter_50Hz_Servo_ZR)

# Grafische Ausgabe der dataframes:

# Vergleich von ACS712 mit und ohne Filter:
#functions_plotly.showlineplot(y_axes='Strom[bit]',dataframes_list=list_USS_ACS712_withfilter_50Hz_Servo_ZR,title='ACS712 mit Filter')
#functions_plotly.showlineplot(y_axes='Strom[bit]',dataframes_list=list_USS_ACS712_withoutfilter_50Hz_Servo_ZR,title='ACS712 ohne Filter')

# Vergleich von INA219 mit und ohne Filter:
functions_plotly.showlineplot(y_axes='Strom[mA]',dataframes_list=list_USS_INA219_withfilter_50Hz_Servo_ZR,title='INA219 mit Filter')
functions_plotly.showlineplot(y_axes='Strom[mA]',dataframes_list=list_USS_INA219_withoutfilter_50Hz_Servo_ZR,title='INA219 ohne Filter')

#INA219 Filter nochmals genau abchecken; da keine großen Unterschiede zwischen den Messwerten bestehen



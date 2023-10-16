# main_VergleichSensoren:
import pandas as pd
import matplotlib.pyplot as plt

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
    ordner='20231016__Laser_INA219_50Hz_Servo_ZR', filter=True,Nullpunkt_current=512)

correct_dataframes_list_2 = functions_pandas.doallpandasfunction(ordner='20231016__Laser_INA219_50Hz_Schritt_ZR', filter=False,Nullpunkt_current=524)



# Ausgabe der dataframes Liste
#print(correct_dataframes_list_1)


# Grafische Verarbeitung der dataframes Liste:

# Plotly Funktionen
#functions_plotly.showlineplot(y_axes='Strom[mA]', dataframes_list=correct_dataframes_list_1, title='Strom_Servo_ZR')
#functions_plotly.showlineplot(y_axes='Strom[mA]', dataframes_list=correct_dataframes_list_2, title='Strom_Schritt_ZR')

# Matplotlib Funktionen:
#Position:
#functions_matplotlib.savelineplot(y_axes='Position[mm]',dataframes_list=correct_dataframes_list_2,title='Position_Schritt_ZR')
#Strom: Servo
#functions_matplotlib.savelineplot(y_axes='Strom[mA]',dataframes_list=correct_dataframes_list_1,title='Strom_Servo_ZR')
#Strom: Schritt
#functions_matplotlib.savelineplot(y_axes='Strom[mA]',dataframes_list=correct_dataframes_list_2,title='Strom_Schritt_ZR')

#Vergleich Servo & Schritt:
servo = correct_dataframes_list_1[7]
schritt = correct_dataframes_list_2[0]

#functions_matplotlib.comparelineplot(y_axes='Strom[mA]',dataframe_servo=servo,dataframe_schritt=schritt,title='Vergleich Stroooom')







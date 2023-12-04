
# test_pandas_plotly:
# .py Datei zum Testen von neuen plotly-Funktionen

# Aktuell: Vergleich der Stromsensoren

# !!!!
# ACHTUNG: es muss ganz genau auf die korrekten Indices geachtet werden
# !!!!

# NUR DA UM DIE GRAFISCHEN FUNKTIONEN ZU SICHERN

# Grafische Ausgabe der dataframes:

# Vergleich von ACS712 mit und ohne Filter:
#functions_plotly.showlineplot(y_axes='Strom[bit]',dataframes_list=list_USS_ACS712_withfilter_50Hz_Servo_ZR,title='ACS712 mit Filter')
#functions_plotly.showlineplot(y_axes='Strom[bit]',dataframes_list=list_USS_ACS712_withoutfilter_50Hz_Servo_ZR,title='ACS712 ohne Filter')

# Vergleich von INA219 mit und ohne Filter:
#functions_plotly.showlineplot(y_axes='Strom[mA]',dataframes_list=list_USS_INA219_withfilter_50Hz_Servo_ZR,title='INA219 mit Filter')
#functions_plotly.showlineplot(y_axes='Strom[mA]',dataframes_list=list_USS_INA219_withoutfilter_50Hz_Servo_ZR,title='INA219 ohne Filter')

#INA219 Filter nochmals genau abchecken; da keine großen Unterschiede zwischen den Messwerten bestehen

# Vergleich der Position (nur USS aktuell):
#functions_plotly.showlineplot(y_axes='Position[cm]',dataframes_list=list_USS_ACS712_withfilter_50Hz_Servo_ZR,title='Position (ACS712 mit Filter)')
#functions_plotly.showlineplot(y_axes='Position[cm]',dataframes_list=list_USS_ACS712_withoutfilter_50Hz_Servo_ZR,title='Position (ACS712 ohne Filter)')
#functions_plotly.showlineplot(y_axes='Position[cm]',dataframes_list=list_USS_INA219_withfilter_50Hz_Servo_ZR,title='Position (INA219 mit Filter)')
#functions_plotly.showlineplot(y_axes='Position[cm]',dataframes_list=list_USS_INA219_withoutfilter_50Hz_Servo_ZR,title='Position (INA219 ohne Filter)')


# Grafische Ausgabe für ppt:

# Vergleich von ACS712 mit und ohne Filter:
#functions_matplotlib.savelineplot(y_axes='Strom[bit]',dataframes_list=list_USS_ACS712_withfilter_50Hz_Servo_ZR,title='ACS712 mit C-Filter')
#functions_matplotlib.savelineplot(y_axes='Strom[bit]',dataframes_list=list_USS_ACS712_withoutfilter_50Hz_Servo_ZR,title='ACS712 ohne Filter')

# Vergleich von INA219 mit und ohne Filter:
#functions_matplotlib.savelineplot(y_axes='Strom[mA]',dataframes_list=list_USS_INA219_withfilter_50Hz_Servo_ZR,title='INA219 mit C-Filter')
#functions_matplotlib.savelineplot(y_axes='Strom[mA]',dataframes_list=list_USS_INA219_withoutfilter_50Hz_Servo_ZR,title='INA219 ohne Filter')

# Vergleich der Position (nur USS aktuell):

#functions_matplotlib.savelineplot(y_axes='Position[cm]',dataframes_list=list_USS_ACS712_withoutfilter_50Hz_Servo_ZR,title='Position mit Ultraschallsensor HC-SR04 (ohne Filter)')
#functions_matplotlib.savelineplot(y_axes='Position[cm]',dataframes_list=list_USS_ACS712_withfilter_50Hz_Servo_ZR,title='Position mit Ultraschallsensor HC-SR04 (mit C-Filter)')

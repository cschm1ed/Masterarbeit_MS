import pandas as pd


def getposition(df):
    counter = 0
    nochange = 0
    errors = 0
    for i in range(len(df) - 1):
        current = df.iloc[i + 1][['Channel 4', 'Channel 5']].values
        previous = df.iloc[i][['Channel 4', 'Channel 5']].values
        # Ohne NoChanges & Errors
        if (current == (0, 0)).all() and (previous == (0, 1)).all():
            counter += 1
        if (current == (0, 0)).all() and (previous == (1, 0)).all():
            counter -= 1

        if (current == (0, 1)).all() and (previous == (0, 0)).all():
            counter -= 1
        if (current == (0, 1)).all() and (previous == (1, 1)).all():
            counter += 1

        if (current == (1, 0)).all() and (previous == (0, 0)).all():
            counter += 1
        if (current == (1, 0)).all() and (previous == (1, 1)).all():
            counter -= 1

        if (current == (1, 1)).all() and (previous == (0, 1)).all():
            counter -= 1
        if (current == (1, 1)).all() and (previous == (1, 0)).all():
            counter += 1

        # Mit NoChanges & Errors
        # NoChanges:
        if (current == (0, 0)).all() and (previous == (0, 0)).all():
            nochange += 1
        if (current == (0, 1)).all() and (previous == (0, 1)).all():
            nochange += 1
        if (current == (1, 0)).all() and (previous == (1, 0)).all():
            nochange += 1
        if (current == (1, 1)).all() and (previous == (1, 1)).all():
            nochange += 1
        # Errors:
        if (current == (0, 0)).all() and (previous == (1, 1)).all():
            errors += 1
        if (current == (0, 1)).all() and (previous == (1, 0)).all():
            errors += 1
        if (current == (1, 0)).all() and (previous == (0, 1)).all():
            errors += 1
        if (current == (1, 1)).all() and (previous == (0, 0)).all():
            errors += 1

    return counter, nochange, errors

# Dateipfad zur CSV-Datei
# Richtung Modell_Stecker
dateiname1 = 'raw_data_sorted/test_LogicAnalyzer/Glasmaßstab/Richtung Modell_Stecker/digital_20cm.csv'
dateiname2 = 'raw_data_sorted/test_LogicAnalyzer/Glasmaßstab/Richtung Modell_Stecker/digital_20cm_2.csv'
dateiname3 = 'raw_data_sorted/test_LogicAnalyzer/Glasmaßstab/Richtung Modell_Stecker/digital_20cm_mitPausen.csv'
# Richtung Fenster_Kabel
dateiname4 = 'raw_data_sorted/test_LogicAnalyzer/Glasmaßstab/Richtung Fenster_Kabel/digital_19cm.csv'
dateiname5 = 'raw_data_sorted/test_LogicAnalyzer/Glasmaßstab/Richtung Fenster_Kabel/digital_20cm_1.csv'
dateiname6 = 'raw_data_sorted/test_LogicAnalyzer/Glasmaßstab/Richtung Fenster_Kabel/digital_20cm_2.csv'


# Einlesen in ein Pandas dataframe
df1 = pd.read_csv(dateiname1)
df2 = pd.read_csv(dateiname2)
df3 = pd.read_csv(dateiname3)
df4 = pd.read_csv(dateiname4)
df5 = pd.read_csv(dateiname5)
df6 = pd.read_csv(dateiname6)

# Aufrufen der Funktionen
counter1, nochange1, error1 = getposition(df1)
print("df1 fertig")
counter2, nochange2, error2 = getposition(df2)
print("df2 fertig")
counter3, nochange3, error3 = getposition(df3)
print("df3 fertig")
counter4, nochange4, error4 = getposition(df4)
print("df4 fertig")
counter5, nochange5, error5 = getposition(df5)
print("df5 fertig")
counter6, nochange6, error6 = getposition(df6)
print("df6 fertig")

# Ausgabe der counter, nochange & errors

print("Modell_Stecker digital_20cm", counter1, nochange1, error1)
print("Modell_Stecker digital_20cm_2", counter2, nochange2, error2)
print("Modell_Stecker digital_20cm_mitPausen", counter3, nochange3, error3)
print("Fenster_Kabel digital_19cm", counter4, nochange4, error4)
print("Fenster_Kabel digital_20cm_1", counter5, nochange5, error5)
print("Fenster_Kabel digital_20cm_2", counter6, nochange6, error6)






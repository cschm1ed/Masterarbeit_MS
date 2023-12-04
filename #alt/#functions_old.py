# alle Ordnername ausgeben bekommen:
def getallfoldernames():
    verzeichnis = 'raw_data_sorted'

    if os.path.exists(verzeichnis) and os.path.isdir(verzeichnis):
        ordner = [d for d in os.listdir(verzeichnis) if os.path.isdir(os.path.join(verzeichnis, d))]
        # hier werden die Ordnernamen noch ausgegeben:
        #for ordnername in ordner:
            #print(ordnername)
    else:
        print(f"Das Verzeichnis '{verzeichnis}' existiert nicht oder ist kein Verzeichnis.")

    return ordner

# Serielle Datenaufnahme 115200baud:
def startDatalogging_115200(name,erfassungsdauer,iteration):
    # Serielle Kommunikation starten + Baudrate festlegen (muss mit Arduino Sketch übereinstimmen)
    ser = serial.Serial('COM5', 115200)
    # Aktuelle Datum + Uhrzeit ermitteln
    jetzt = datetime.datetime.now()
    # Ordner festlegen, in welchem die Daten gespeichert werden
    ordnername = "raw_data_unsorted"
    # Dateinamen mit Datum und Uhrzeit erstellen
    # hier müssen auch weitere Details eingetragen werden, bzw. im Funktionsaufruf
    dateiname = os.path.join(ordnername, jetzt.strftime("%Y-%m-%d_%H-%M-%S") + "_" + name + ".txt")
    # hier wird die eigentliche Referenzfahrt gestartet
    startRunningCNC()

    with open(dateiname, 'w') as file:
        startzeit = time.time()  # Startzeit erfassen
        # while True:
        while (time.time() - startzeit) < erfassungsdauer:
            try:
                line = ser.readline().decode().strip()
            except UnicodeDecodeError:
                line = '9999.99,999999,9999999'
                print('         UnicodeDecodeFehler Referenzfahrt_' + str(iteration))
            file.write(line + '\n')
    ser.close()
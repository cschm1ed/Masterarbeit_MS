# ----
# MAIN: STARTEN VON n-REFERENZFAHRTEN
# ----

import time
from tqdm import tqdm
import functions.logicanalyzer as LogicAnalyzer
import functions.estlcam as Estlcam
import functions.general as General

# Abfahren von n Referenzfahrten, automatisiert hintereinander
# Hauptanzeige muss der Laptop sein (nicht der Bildschirm)

# Anzahl der Referenzfahrten:
n = 10

# Dauer einer einzelnen Referenzfahrt (für die Datenaufnahme)
# v2: 75s
# v3: 120s
dauer = 120

# Benutzte Teile:
motor = 'Servomotor'
getriebe = 'Zahnriemen'

# Öffnen von Logic2 & Estlcam
prozess_Logic2 = LogicAnalyzer.startLogic2()
prozess_Estlcam = Estlcam.openEstlcam()
Estlcam.openReferenceRun()

# Mail beim Start senden
General.sendMail(recieveradress='maxi11696@googlemail.com', iteration=0, numberofdrives=n)
# durch Anzahl der Referenzfahrten iterieren
for i in range(1, n+1):
    print("--- Start Referenzfahrt " + str(i) + "/" + str(n) + ":\t" + motor + " - " + getriebe)
    # Start der Datenaufnahme und der Referenzfahrt
    LogicAnalyzer.recordData_Logic2(dauer=dauer, motor=motor, getriebe=getriebe)
    print("\t.... Referenzfahrt " + str(i) + "/" + str(n) + " done")
    # Mail senden
    if i % 5 == 0 and i != n:
        General.sendMail(recieveradress='maxi11696@googlemail.com', iteration=i, numberofdrives=n)
        print('\n--- Pause: 90s')
        for j in tqdm(range(1, 91)):
            time.sleep(1)
        print('\n')
    # Mail senden nach Abschluss
    if i == n:
        General.sendMail(recieveradress='maxi11696@googlemail.com', iteration=i, numberofdrives=n)
    # Pause zum Abkühlen von Motor & Spindel
    time.sleep(10)

print("\nReferenzfahrten (" + str(n) + ") erfolgreich abgeschlossen. ---")
# Schließen von Logic2 & Estlcam
prozess_Estlcam.terminate()
prozess_Logic2.terminate()

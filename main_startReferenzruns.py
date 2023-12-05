# ----
# MAIN: STARTEN VON n-REFERENZFAHRTEN
# ----

import time
import functions_general
import functions_logicanalyzer

# Abfahren von n Referenzfahrten, automatisiert hintereinander
# Hauptanzeige muss der Laptop sein (nicht der Bildschirm)

# Anzahl der Referenzfahrten:
n = 2

# Dauer einer einzelnen Referenzfahrt (für die Datenaufnahme)
dauer = 50

# Benutzte Teile:
motor = 'Schrittmotor'
getriebe = 'Zahnriemen'

# Öffnen von Logic2 & Estlcam
prozess_Logic2 = functions_logicanalyzer.startLogic2()
prozess_Estlcam = functions_general.openEstlcam()
functions_general.openReferenzrun()

# Mail beim Start senden
functions_general.sentMail('maxi11696@googlemail.com',iteration=0,numberofdrives=n)
# durch Anzahl der Referenzfahrten iterieren
for i in range(1, n+1):
    print("--- Start Referenzfahrt " + str(i) + "/" + str(n) + ":\t" + motor + " - " + getriebe)
    # Start der Datenaufnahme und der Referenzfahrt
    functions_logicanalyzer.recordLogic2Data(dauer=dauer, motor=motor, getriebe=getriebe)
    print("     .... Referenzfahrt " + str(i) + "/" + str(n) + " done")
    # Mail senden
    if i % 5 == 0 or i == n:
        functions_general.sentMail('maxi11696@googlemail.com',iteration=i,numberofdrives=n)
    # Pause zum Abkühlen von Motor & Spindel
    time.sleep(10)

print("Referenzfahrten (" + str(n) + ") erfolgreich abgeschlossen. ---")
# Schließen von Logic2 & Estlcam
prozess_Estlcam.terminate()
prozess_Logic2.terminate()

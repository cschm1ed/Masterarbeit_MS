# main_startReferenzruns:

# Abfahren von n Referenzfahrten, automatisiert hintereinander
# aktuell mit Abtastrate von 50 Hz; aufgrund des USS

# Import der ganzen Funktionen:
import time
import functions_general


# Anzahl der Referenzfahrten:
n=1

prozess = functions_general.open_Estlcam()
functions_general.openReferenzrun()

print("--- Start Referenzfahrt: ---")
functions_general.sentMail('maxi11696@googlemail.com',iteration=0,numberofdrives=n)
for i in range(1,n+1):
    name = "Referenzfahrt_" + str(i)
    # hier muss neue Funktion angepasst werden
    functions_general.startDatalogging_115200(name=name,erfassungsdauer=60,iteration=i)
    print("     ...." + name + " done")
    if i % 5 == 0:
        functions_general.sentMail('maxi11696@googlemail.com',iteration=i,numberofdrives=n)
    time.sleep(10)

prozess.terminate()

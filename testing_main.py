# Import der ganzen Funktionen:
import time
import functions


# testing_main
# Aufrufen der Funktion:
# Aktuell mit Abtastrate von 50 Hz; aufgrund des USS

# Anzahl der Referenzfahrten:
n=25

prozess = functions.open_Estlcam()
functions.openReferenzrun()

print("--- Start Referenzfahrt: ---")
for i in range(1,n+1):
    name = "Referenzfahrt_" + str(i)
    functions.startDatalogging_115200(name=name,erfassungsdauer=60,iteration=i)
    print("     ...." + name + " done")
    if i % 5 == 0:
        functions.sentMail('maxi11696@googlemail.com',iteration=i,numberofdrives=n)
    time.sleep(10)

prozess.terminate()

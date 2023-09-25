# Import der ganzen Funktionen:

from functions import open_Estlcam
from functions import startReferenceRun
from functions import startDatalogging_57600

# Aufrufen der Funktion openEslcam
open_Estlcam()
startReferenceRun()
startDatalogging_57600("Funktionstest",10)
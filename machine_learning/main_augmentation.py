from machine_learning.functions_augmentation import *

# Int.funktion erstellen
p = createIntFunktion()

# Synthetische Daten erzeugen und abspeichern
createAugData(p=p,number_runs=5, factor_down=0.2, factor_up=1.8)
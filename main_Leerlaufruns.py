# main_Leerlaufruns:

# Leerlaufrun mit der Länge dauer
# zur Speicherung von Nullwerten, usw.
# aktuell mit Abtastrate von 50 Hz; aufgrund des USS

# Import der ganzen Funktionen:
import functions

# Dauer der Referenzfahrt (in Sekunden):
dauer = 10


functions.startDatalogging_115200(name='Leerlauf_Schaltschrank_on_VergleichLogicAnalyzer',erfassungsdauer=dauer,iteration=1)
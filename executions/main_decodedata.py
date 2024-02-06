import functions.general as General

# ----
# MAIN: Dekodierung & Verarbeitung der aufgenommenen Daten
# ----

# Hier werden die .csv Dateien für Position + Stromstärke erstellt
General.createCSV_CurrentPosition()

# Hier werden die finalen Ordner in #fertig erstellt, sowie die alten Ordner in #alt geschoben
General.moveCSVtofertig()

# Hier werden die finalen Ordner richtig zugeteilt
General.sortFolder()

# Hier eine Übersicht über die Anzahl der jeweiligen Referenzfahrt gegeben
General.countReferenceRuns()

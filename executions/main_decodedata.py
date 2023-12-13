from functions.general import General


# Hier werden die .csv Dateien für Position + Stromstärke erstellt
General.createFilesCurrentPosition()

# Hier werden die finalen Ordner in #fertig erstellt, sowie die alten Ordner in #alt geschoben
General.createFinalFiles()

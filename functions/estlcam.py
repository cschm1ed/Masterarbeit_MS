import subprocess
import pyautogui
import time
import pygetwindow as gw
from configurations.config import Config


# Funktion zum Öffnen von Estlcam & des CNC-Controller:
def openEstlcam():
    # Pfad der Estlcam.exe Datei
    exe_datei_pfad = Config.PATH_estlcam_exe
    # Die ausführbare Datei öffnen
    prozess = subprocess.Popen([exe_datei_pfad])
    # Starten der Mausbewegung:
    time.sleep(8)
    pyautogui.click(220, 30)
    pyautogui.click(220, 100)
    time.sleep(3)
    # Fenster in richtige Position verschieben
    aktives_fenster = gw.getActiveWindow()
    aktives_fenster.moveTo(0, 0)
    pyautogui.click(260, 410)
    time.sleep(3)
    pyautogui.click(1270, 720)
    time.sleep(7)
    # Fenster maximieren
    aktives_fenster = gw.getActiveWindow()
    aktives_fenster.maximize()
    print('Funktion "openEstlcam" abgeschlossen. ---')
    return prozess

# Funktion zum Laden der Referenzfahrt:
def openReferencenRun():
    time.sleep(3)
    aktives_fenster = gw.getActiveWindow()
    fenstertitel = aktives_fenster.title
    if fenstertitel == "Estlcam 11,245_A_64":
        time.sleep(2)
        pyautogui.click(1590, 1030)
        time.sleep(3)
        pyautogui.click(1875, 50)
        time.sleep(3)
        # Fenster in richtige Position verschieben
        aktives_fenster = gw.getActiveWindow()
        aktives_fenster.moveTo(0, 0)
        time.sleep(3)
        pyautogui.doubleClick(750, 160)
        time.sleep(12)
        pyautogui.click(1160, 660)
        time.sleep(3)
        print('Funktion "openReferenceRun" abgeschlossen. ---')
    else:
        print("Fehler: CNC-Controller nicht richtig geöffnet. ---")

# Funktion zum Starten der Referenzfahrt:
def startReferenceRun():
    time.sleep(1)
    pyautogui.click(1605, 1057)
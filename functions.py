import subprocess
import pyautogui
import time
import pygetwindow as gw
import serial
import datetime
import os


# Hier wird Estlcam und der CNC-Controller geöffnet:
def open_Estlcam():
    # Pfad der Estlcam.exe Datei
    exe_datei_pfad = "C:\\Users\\maxi1\\Documents\\UNI MASTER KIT\\#MASTERARBEIT\\05 Sonstige Dokumente\\Estlcam11\\Estlcam.exe"
    # Die ausführbare Datei öffnen
    subprocess.Popen([exe_datei_pfad])
    # Starten der Mausbewegung:
    time.sleep(8)
    pyautogui.click(220, 30)
    pyautogui.click(220, 100)
    time.sleep(1)
    # Fenster in richtige Position verschieben
    aktives_fenster = gw.getActiveWindow()
    aktives_fenster.moveTo(0, 0)
    pyautogui.click(260, 410)
    time.sleep(1)
    pyautogui.click(1270, 720)
    time.sleep(5)
    # Fenster maximieren
    aktives_fenster = gw.getActiveWindow()
    aktives_fenster.maximize()

# Hier wird im CNC-Controller die Referenzfahrt gestartet:
def startReferenceRun():
    time.sleep(3)
    aktives_fenster = gw.getActiveWindow()
    fenstertitel = aktives_fenster.title
    if fenstertitel == "Estlcam 11,245_A_64":
        time.sleep(2)
        pyautogui.click(1590, 1030)
        time.sleep(1)
        pyautogui.click(1875, 50)
        time.sleep(1)
        # Fenster in richtige Position verschieben
        aktives_fenster = gw.getActiveWindow()
        aktives_fenster.moveTo(0, 0)
        time.sleep(1)
        pyautogui.doubleClick(750, 160)
        time.sleep(8)
        pyautogui.click(1150, 660)
        time.sleep(2)
        pyautogui.click(1120,655)
        time.sleep(1)
        pyautogui.click(1605, 1057)
    else:
        print("CNC-Controller nicht richtig geöffnet.")

# Serielle Datenaufnahme:
def startDatalogging_57600(name,erfassungsdauer):
    # Serielle Kommunikation starten + Baudrate festlegen (muss mit Arduino Sketch übereinstimmen)
    ser = serial.Serial('COM5', 57600)
    # Aktuelle Datum + Uhrzeit ermitteln
    jetzt = datetime.datetime.now()
    # Ordner festlegen, in welchem die Daten gespeichert werden
    ordnername = "txt_Daten"
    # Dateinamen mit Datum und Uhrzeit erstellen
    # hier müssen auch weitere Details eingetragen werden
    dateiname = os.path.join(ordnername, jetzt.strftime("%Y-%m-%d_%H-%M-%S") + "_" + name + ".txt")
    try:
        with open(dateiname, 'w') as file:
            startzeit = time.time()  # Startzeit erfassen
            # while True:
            while (time.time() - startzeit) < erfassungsdauer:
                line = ser.readline().decode().strip()
                print(line)
                file.write(line + '\n')
    except KeyboardInterrupt:
        print("Erfassung von Daten wurde gestoppt (Strg+C gedrückt).")
    finally:
        ser.close()
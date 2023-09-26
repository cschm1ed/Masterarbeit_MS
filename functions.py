import subprocess
import pyautogui
import time
import pygetwindow as gw
import serial
import datetime
import os
import pandas as pd

# für Mail:
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# Hier wird Estlcam und der CNC-Controller geöffnet:
def open_Estlcam():
    # Pfad der Estlcam.exe Datei
    exe_datei_pfad = "C:\\Users\\maxi1\\Documents\\UNI MASTER KIT\\#MASTERARBEIT\\05 Sonstige Dokumente\\Estlcam11\\Estlcam.exe"
    # Die ausführbare Datei öffnen
    prozess = subprocess.Popen([exe_datei_pfad])
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
    return prozess

# Hier wird der CNC-Controller geöffnet:
def openReferenzrun():
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
    else:
        print("CNC-Controller nicht richtig geöffnet.")

#Hier wird die Referenzfahrt gestartet:
def startRunningCNC():
    time.sleep(1)
    pyautogui.click(1605, 1057)

# Serielle Datenaufnahme 115200baud:
def startDatalogging_115200(name,erfassungsdauer):
    # Serielle Kommunikation starten + Baudrate festlegen (muss mit Arduino Sketch übereinstimmen)
    ser = serial.Serial('COM5', 115200)
    # Aktuelle Datum + Uhrzeit ermitteln
    jetzt = datetime.datetime.now()
    # Ordner festlegen, in welchem die Daten gespeichert werden
    ordnername = "txt_Daten"
    # Dateinamen mit Datum und Uhrzeit erstellen
    # hier müssen auch weitere Details eingetragen werden
    dateiname = os.path.join(ordnername, jetzt.strftime("%Y-%m-%d_%H-%M-%S") + "_" + name + ".txt")
    startRunningCNC()

    with open(dateiname, 'w') as file:
        startzeit = time.time()  # Startzeit erfassen
        # while True:
        while (time.time() - startzeit) < erfassungsdauer:
            try:
                line = ser.readline().decode().strip()
            except UnicodeDecodeError:
                line = '9999.99,999999,9999999'
                print('         ....UnicodeDecodeFehler')
            file.write(line + '\n')
    ser.close()

# Serielle Datenaufnahme 57600baud:
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

# Speichern der txt-Daten in pandas dataframe:
def saveasDataframe():
    # Ordnerpfad festlegen
    ordnername = "txt_Daten"

    # Leere Liste erstellen, um Datenframes zu speichern
    alle_daten = []

    # Durch alle Dateien im Ordner iterieren
    for index, dateiname in enumerate(os.listdir(ordnername)):
        if dateiname.endswith(".txt"):  # Prüfen, ob es sich um eine Textdatei handelt
            dateipfad = os.path.join(ordnername, dateiname)

            try:
                # Einlesen der TXT-Datei mit read_table
                data = pd.read_table(dateipfad, delim_whitespace=True)

                # Neue Spaltennamen zuweisen
                #new_columns = ['Stromstärke [mA]', 'Position [mm]']
                #data.columns = new_columns

                # Berechnung durchführen
                # Position
                #data['Position [mm]'] = data['Position [mm]'] / 2 * 0.3432  # Umrechnen der Dauer in Position
                #data['Position [mm]'] = data['Position [mm]'] - (734.65 / 2 * 0.3432)  # Nullpunkt festlegen


                # Das Datenframe zur Liste hinzufügen
                alle_daten.append(data)


            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei: {dateipfad}")
                continue  # Zur nächsten Datei springen
    # Rückgabe der Lista aller Daten
    return alle_daten

# Mail schicken:
def sentMail(recieveradress,iteration):
    now = datetime.datetime.now()
    mail_content = now.strftime("%m/%d/%Y, %H:%M:%S") + ' Referenzfahrt: ' + str(iteration)
    # The mail addresses and password
    sender_address = 'stephantest691@gmail.com'
    sender_pass = 'oooldqiehttcuzsc'
    receiver_address = recieveradress
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = mail_content
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()



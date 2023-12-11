# ----
# FUNKTIONEN ZUR STEUERUNG VON ESTLCAM (DER REFERENZFAHRTEN) & WEITERE ALLGEMEINE FUNKTIONEN
# ----

import subprocess
import pyautogui
import time
import pygetwindow as gw
import datetime
import functions_decodedata
import os
import shutil

# für Mail:
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Funktion zum Öffnen von Estlcam & des CNC-Controller:
def openEstlcam():
    # Pfad der Estlcam.exe Datei
    exe_datei_pfad = "C:\\Users\\maxi1\\Documents\\UNI MASTER KIT\\#MASTERARBEIT\\05 Sonstige Dokumente\\Estlcam11\\Estlcam.exe"
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
def openReferenzrun():
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
        print('Funktion "openReferenzrun" abgeschlossen. ---')
    else:
        print("Fehler: CNC-Controller nicht richtig geöffnet. ---")

# Funktion zum Starten der Referenzfahrt:
def startReferenzrun():
    time.sleep(1)
    pyautogui.click(1605, 1057)


# Funktion zum automatisierten Mails schicken:
def sentMail(recieveradress,iteration,numberofdrives):
    now = datetime.datetime.now()
    mail_content = now.strftime("%m/%d/%Y, %H:%M:%S") + ' Referenzfahrt: ' + str(iteration) + '/' + str(numberofdrives)
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


# Funktion zur Erstellung der Dateien current.csv & position.csv
def createFilesCurrentPosition():

    ordner_liste = [d for d in os.listdir("raw_data_sorted") if os.path.isdir(os.path.join("raw_data_sorted", d)) and "digital_output" in d]

    for ordner in ordner_liste:
        verzeichnis = 'raw_data_sorted\\' + ordner
        print('--- ' + verzeichnis + ':')

        verzeichnis_position = os.path.join(verzeichnis, 'digital.csv')
        df_position = functions_decodedata.decodePosition(verzeichnis_position)
        df_position.to_csv(verzeichnis + '\\position.csv', index=False)

        verzeichnis_current = os.path.join(verzeichnis, 'i2c_export.csv')
        df_current = functions_decodedata.decodeCurrent(verzeichnis_current)
        df_current.to_csv(verzeichnis + '\\current.csv', index=False)

    print('--- Für alle Ordner in "raw_data_sorted" wurden die Dateien current.csv und position.csv erstellt.')

# Funktion zur finalen Datenerstellung
def createFinalFiles():
    ordner_liste = [d for d in os.listdir("raw_data_sorted") if
                        os.path.isdir(os.path.join("raw_data_sorted", d)) and "digital_output" in d]

    # Checken, ob die dateinamen in den Ordnern vorhanden sind
    for ordner in ordner_liste:
        verzeichnis = 'raw_data_sorted\\' + ordner
        dateinamen = ['current.csv', 'position.csv', 'i2c_export.csv', 'digital.csv', 'used_parts.txt']
        alle_vorhanden = True
        for dateiname in dateinamen:
            pfad_zur_datei = os.path.join(verzeichnis, dateiname)
            if not os.path.isfile(pfad_zur_datei):
                alle_vorhanden = False
                break


        # Zugriff auf Daten der Messung
        with open(verzeichnis + '\\used_parts.txt', 'r') as file:
            lines = file.readlines()
            txt_name_motor_list = lines[2].split(' ',1)
            txt_name_getriebe_list = lines[3].split(' ',1)
            txt_time = lines[6]

            txt_name_motor = txt_name_motor_list[1]
            txt_name_getriebe = txt_name_getriebe_list[1]

        print('--- ' + verzeichnis + ':')
        if alle_vorhanden:
            print('\t.... Dateien ("current.csv", "position.csv", "i2c_export.csv", "digital.csv", "used_parts.txt") sind vorhanden.')
        else:
            print('\t.... Fehler: Nicht alle Dateien sind vorhanden.')

        # Dateien 'current.csv', 'position.csv', 'used_parts.txt' in neuen Ordner (mit Name txt_time) in Ordner #fertig kopieren
        ziel_pfad = 'raw_data_sorted\\#fertig\\' + txt_time # Ersetze dies durch den Pfad des neuen Ordners, den du erstellen möchtest

        if not os.path.exists(ziel_pfad):
            os.makedirs(ziel_pfad)
            print(f"\t.... Ordner {ziel_pfad} wurde erfolgreich erstellt.")
        else:
            print(f"\t.... Ordner {ziel_pfad} existiert bereits.")

        dateien = ['current.csv', 'position.csv', 'used_parts.txt']  # Liste der Dateinamen

        for datei in dateien:
            quelle_datei_pfad = os.path.join(verzeichnis, datei)
            ziel_datei_pfad = os.path.join(ziel_pfad, datei)
            shutil.copyfile(quelle_datei_pfad, ziel_datei_pfad)
        print('\t.... Dateien ("current.csv", "position.csv", "used_parts.txt") wurden erfolgreich hinzugefügt.')

        # Ordner 'digital_output_' in #alt bewegen
        pfad_ordner_alt = 'raw_data_sorted\\#alt'
        shutil.move(verzeichnis, pfad_ordner_alt)
        print('\t.... Ordnern wurde in den Pfad #alt verschoben.')

    print('--- Für alle Ordner in "raw_data_sorted" wurden #fertig Ordner erstellt, sowie die Ordner in den Pfad #alt verschoben.')

# Funktion, welche die Fahrten nach Kombinationen ordnet
# todo: muss noch komplett geschrieben werden




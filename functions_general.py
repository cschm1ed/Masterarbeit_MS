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
    return prozess

# Hier wird der CNC-Controller geöffnet:
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
        time.sleep(8)
        pyautogui.click(1150, 660)
        time.sleep(4)
        pyautogui.click(1120,655)
    else:
        print("CNC-Controller nicht richtig geöffnet.")

#Hier wird die Referenzfahrt gestartet:
def startRunningCNC():
    time.sleep(1)
    pyautogui.click(1605, 1057)


# Mail schicken:
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





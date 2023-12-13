
import datetime
import os
import shutil
import functions.decodedata as DecodeData
from configurations.config import Config

# für Mail:
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# Funktion zum automatisierten Mails schicken:
def sendMail(recieveradress, iteration, numberofdrives):
    now = datetime.datetime.now()
    mail_content = now.strftime("%m/%d/%Y, %H:%M:%S") + ' Referenzfahrt: ' + str(iteration) + '/' + str(
        numberofdrives)
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
def createCSV_CurrentPosition():

    ordner_liste = [d for d in os.listdir(Config.PATH_raw_data) if
                    os.path.isdir(os.path.join(Config.PATH_raw_data, d)) and "digital_output" in d]
    if ordner_liste:
        for ordner in ordner_liste:
            verzeichnis = os.path.join(Config.PATH_raw_data, ordner)
            print('--- ' + verzeichnis + ':')

            verzeichnis_position = os.path.join(verzeichnis, 'digital.csv')
            df_position = DecodeData.decodePosition(dateipfad=verzeichnis_position)
            df_position.to_csv(os.path.join(verzeichnis, 'position.csv'), index=False)

            verzeichnis_current = os.path.join(verzeichnis, 'i2c_export.csv')
            df_current = DecodeData.decodeCurrent(dateipfad=verzeichnis_current)
            df_current.to_csv(os.path.join(verzeichnis, 'current.csv'), index=False)

        print('--- Für alle Ordner in "raw_data_sorted" wurden die Dateien "current.csv" und "position.csv" erstellt.')
    else:
        print('--- Keine rohen Daten (digital_output) vorhanden.')

# Funktion zur finalen Datenerstellung
def moveCSVtofertig():
    ordner_liste = [d for d in os.listdir(Config.PATH_raw_data) if
                    os.path.isdir(os.path.join(Config.PATH_raw_data, d)) and "digital_output" in d]
    if ordner_liste:
        # Checken, ob die dateinamen in den Ordnern vorhanden sind
        for ordner in ordner_liste:
            verzeichnis = os.path.join(Config.PATH_raw_data, ordner)
            dateinamen = ['current.csv', 'position.csv', 'i2c_export.csv', 'digital.csv', 'used_parts.txt']
            alle_vorhanden = True
            for dateiname in dateinamen:
                pfad_zur_datei = os.path.join(verzeichnis, dateiname)
                if not os.path.isfile(pfad_zur_datei):
                    alle_vorhanden = False
                    break

            # Zugriff auf Daten der Messung
            with open(os.path.join(verzeichnis, 'used_parts.txt'), 'r') as file:
                lines = file.readlines()
                txt_name_motor_list = lines[2].split(' ', 1)
                txt_name_getriebe_list = lines[3].split(' ', 1)
                txt_time = lines[6]

                txt_name_motor = txt_name_motor_list[1]
                txt_name_getriebe = txt_name_getriebe_list[1]

            print('--- ' + verzeichnis + ':')
            if alle_vorhanden:
                print(
                    '\t.... Dateien ("current.csv", "position.csv", "i2c_export.csv", "digital.csv", "used_parts.txt") sind vorhanden.')
            else:
                print('\t.... Fehler: Nicht alle Dateien sind vorhanden.')

            # Dateien 'current.csv', 'position.csv', 'used_parts.txt' in neuen Ordner (mit Name txt_time) in Ordner #fertig kopieren
            ziel_pfad = os.path.join(Config.PATH_data_fertig, txt_time)

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
            shutil.move(verzeichnis, Config.PATH_data_alt)
            print('\t.... Ordnern wurde in den Pfad #alt verschoben.')

        print(
            '--- Finale Ordner in "raw_data_sorted/#fertig" wurden erstellt und gefüllt, sowie die Ordner (digital_ouput) gelöscht.')
    else:
        print('--- Keine rohen Daten (digital_output) vorhanden.')

# Funktion, welche die Anzahl der durchgeführten Referenzfahrt zählt
def countReferenceRuns():
    counter_servo_raeder = 0
    counter_servo_riemen = 0
    counter_schritt_raeder = 0
    counter_schritt_riemen = 0

    ordner_liste = [d for d in os.listdir(Config.PATH_data_fertig) if
                    os.path.isdir(os.path.join(Config.PATH_data_fertig, d))]

    for ordner in ordner_liste:
        verzeichnis = os.path.join(Config.PATH_data_fertig, ordner)
        ordner_liste_2 = [d for d in os.listdir(verzeichnis) if
                          os.path.isdir(os.path.join(verzeichnis, d))]
        for ordner_2 in ordner_liste_2:
            verzeichnis_2 = os.path.join(verzeichnis, ordner_2)
            with open(os.path.join(verzeichnis_2, 'used_parts.txt'), 'r') as file:
                inhalt = file.read()
                if 'Servo' in inhalt and 'Zahnräder' in inhalt:
                    counter_servo_raeder = counter_servo_raeder + 1
                elif 'Schritt' in inhalt and 'Zahnräder' in inhalt:
                    counter_schritt_raeder = counter_schritt_raeder + 1
                elif 'Servo' in inhalt and 'Zahnriemen' in inhalt:
                    counter_servo_riemen = counter_servo_riemen + 1
                elif 'Schritt' in inhalt and 'Zahnriemen' in inhalt:
                    counter_schritt_riemen = counter_schritt_riemen + 1

    print('\nAnzahl der jeweils durchgeführten Referenzfahrten:\n')
    print('Servomotor_Zahnräder:\t\t' + str(counter_servo_raeder))
    print('Schrittmotor_Zahnräder:\t\t' + str(counter_schritt_raeder))
    print('Servomotor_Zahnriemen:\t\t' + str(counter_servo_riemen))
    print('Schrittmotor_Zahnriemen:\t' + str(counter_schritt_riemen))
    counter = counter_schritt_raeder + counter_servo_riemen + counter_schritt_raeder + counter_schritt_riemen
    print('\nGesamt:\t\t\t\t\t\t' + str(counter))

# Funktion, welche die Fahrten nach Kombinationen ordnet
def sortFolder():
    ordner_liste = [d for d in os.listdir(Config.PATH_data_fertig) if
                    os.path.isdir(os.path.join(Config.PATH_data_fertig, d)) and "#_" not in d]
    if ordner_liste:
        for ordner in ordner_liste:
            verzeichnis = os.path.join(Config.PATH_data_fertig, ordner)

            with open(os.path.join(verzeichnis, 'used_parts.txt'), 'r') as file:
                inhalt = file.read()
            if 'Servo' in inhalt and 'Zahnräder' in inhalt:
                shutil.move(verzeichnis, Config.PATH_servo_raeder)
            elif 'Schritt' in inhalt and 'Zahnräder' in inhalt:
                shutil.move(verzeichnis, Config.PATH_schritt_raeder)
            elif 'Servo' in inhalt and 'Zahnriemen' in inhalt:
                shutil.move(verzeichnis, Config.PATH_servo_riemen)
            elif 'Schritt' in inhalt and 'Zahnriemen' in inhalt:
                shutil.move(verzeichnis, Config.PATH_schritt_riemen)

        print('--- Ordnern wurde dem zugehörigen Pfad zugeteilt.')
    else:
        print('--- Keine Ordner vorhanden.')
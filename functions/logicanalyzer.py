from saleae import automation
import os
import os.path
import subprocess
import functions.estlcam as Estlcam
from datetime import datetime
import time
from saleae.automation import RadixType
from saleae.automation import DataTableExportConfiguration
from configurations.config import Config

# ----
# FUNKTIONEN ZUR STEUERUNG VON LOGIC 2
# ----


# Funktion zum Starten von Logic2:
def startLogic2():
    exe_datei_pfad = Config.PATH_logic2_exe
    prozess = subprocess.Popen([exe_datei_pfad])
    time.sleep(10)
    print('Funktion "startLogic2" abgeschlossen: Anwendung Logic2 geöffnet + LogicAnalyzer initialisiert. ---')
    return prozess


# Funktion zum Starten der Datenaufnahme für die Dauer dauer:
def recordData_Logic2(dauer, motor, getriebe):
    # Wichtige Infos:
    # https://saleae.github.io/logic2-automation/

    with automation.Manager.connect(port=10430) as manager:
        device_configuration = automation.LogicDeviceConfiguration(
            enabled_digital_channels=[0, 1, 4, 5],
            # evtl. noch Channel 2 als Trigger (siehe auch unten) & Channel 6 als Z bei Glasmaßstab
            digital_sample_rate=10_000_000,
            # digital_threshold_volts=3.3
        )

        # Aufnahme für die Zeitdauer dauer
        capture_configuration_timecapture = automation.CaptureConfiguration(
            capture_mode=automation.TimedCaptureMode(duration_seconds=dauer)
        )

        # Aufnahme bei Auslösen eines Triggers (Channel 2) & für die Zeitdauer dauer & 2s vor dem Trigger
        # triggertype = automation.DigitalTriggerType.RISING
        # capture_configuration_trigger = automation.CaptureConfiguration(
        # capture_mode=automation.DigitalTriggerCaptureMode(trigger_channel_index=2, trigger_type=triggertype, trim_data_seconds=2, after_trigger_seconds=dauer)
        # )

        with manager.start_capture(
                device_id='A60D1D2452ABF025',  # Logic8 Device
                # device_id='F4241', # für Demo Version
                device_configuration=device_configuration,
                capture_configuration=capture_configuration_timecapture) as capture:
            # Start der Referenzfahrt
            Estlcam.startReferenceRun()
            # Warten bis die capture beendet ist
            capture.wait()

            # I2C Analyzer für die Channel 0 & 1
            i2c_analyzer = capture.add_analyzer('I2C', label=f'I2C', settings={
                'SDA': 1,
                'SCL': 0
            })

            # Ordner erstellen (in welchem die Daten gespeichert werden)
            ordnername = Config.PATH_raw_data
            output_dir = os.path.join(ordnername, f'digital_output-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
            os.makedirs(output_dir)

            # txt Datei mit Motor-, Getriebe-typ, usw. zu Ordner hinzufügen
            txt_file_path = os.path.join(output_dir, 'used_parts.txt')

            # Öffnen der Datei im Schreibmodus ('w' für Schreiben)
            with open(txt_file_path, 'w') as file:
                file.write('Used parts:\n\n')
                file.write('Motor: ' + motor + '\n')
                file.write('Getriebe: ' + getriebe + '\n\n\n')
                file.write(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

            # Konfiguration des export-Analyzer
            radixtype = RadixType.HEXADECIMAL
            config_export_analyzer = DataTableExportConfiguration(analyzer=i2c_analyzer, radix=radixtype)
            # Export von I2C Analyzer Daten
            analyzer_export_filepath = os.path.join(output_dir, 'i2c_export.csv')
            capture.export_data_table(
                filepath=analyzer_export_filepath,
                analyzers=[i2c_analyzer, config_export_analyzer]
            )

            # Export von raw_digital_data für die Channel 4 & 5
            capture.export_raw_data_csv(directory=output_dir, digital_channels=[4, 5])

            # Speichern der capture Datei
            # capture_filepath = os.path.join(output_dir, 'capture.sal')
            # capture.save_capture(filepath=capture_filepath)

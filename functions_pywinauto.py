# Hier werden Funktionen geschrieben, mit welchen Estlcam gesteuert wird

import time

from pywinauto import application
from pywinauto.keyboard import send_keys
from pywinauto.application import Application

from pywinauto import Desktop

# Erstellen Sie ein Desktop-Objekt
desktop = Desktop()

# Geben Sie den Fenstertitel ein, nach dem Sie suchen möchten
fenstertitel = 'Estlcam 11,245_A_64 "G-Code_Test_v2.nc"  / Laufzeit ca. 00:00:00'  # Ersetzen Sie "Ihr_Fenstertitel" durch den tatsächlichen Fenstertitel

# Zugriff auf das Fenster mit dem angegebenen Fenstertitel
#window = desktop.window(title=fenstertitel)

time.sleep(2)

# Öffnen der Anwendung oder Zugriff auf das bereits geöffnete Fenster
app = Application(backend="uia").connect(title=fenstertitel)  # Ersetzen Sie "Fenstertitel" durch den tatsächlichen Fenstertitel

# Zugriff auf das gewünschte Button-Steuerelement mit den angegebenen Kriterien
button = app.window(auto_id="btn_prog_start", control_type="Estlcam.my_Button")

# Klicken Sie auf das Button-Steuerelement
button.click()

window.print_control_identifiers()

# Zugriff auf den Button (ersetzen Sie "Button Text" durch den tatsächlichen Text des Buttons)
#button = main_window.ButtonControl(text="Einstellungen")

# Klicken Sie auf den Button
#button.click()

time.sleep(2)

app.kill()
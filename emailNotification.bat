@ECHO OFF
cd "C:\Users\Jonathan\Desktop\Coding\pythonAutomation\emailNotification"

echo E-Mail Ueberpruefung Anmeldedaten (Uni Account):
set/p "user=Benutzername: "
set/p "pswd=Passwort:     "
python emailNotification.py "%user%" "%pswd%"

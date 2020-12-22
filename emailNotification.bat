::todo -> hide password input

@ECHO OFF
cd "path-to-python-file"

echo E-Mail Ueberpruefung Anmeldedaten (Uni Account):
set/p "user=Benutzername: "
set/p "pswd=Passwort:     "
python emailNotification.py "%user%" "%pswd%"

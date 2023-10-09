# Installatie
Om dit project te kunnen runnen moeten er een aantal dingen geïnstallerd zijn. Dit zijn:
Python: https://www.python.org/
IDE / code editor: https://code.visualstudio.com/
Volg de instructies op de desbetreffende sites voor de installatie.

# Let op! Het kan zijn dat er een foutmelding optreed tijdens het uitvoeren van de volgende commando's. Kijk voor de oplossing bij het kopje: Probleemoplossing.
```
pip install virtualenv
virtualenv venv
.\venv\scripts\activate
pip install -r requirements.txt
```
# De applicatie
Typ de volgende commando's in de terminal om de applicatie te starten: 
``` 
.\venv\scripts\activate
python app.py
```
Wanneer de applicatie gestart wordt kom je terecht op het inlog scherm. In de footer staan nu een aantal links/knoppen. Deze zijn niet functioneel en dienen na in gebruik name van de website naar de betreffende locaties gelinkt te worden.

Nadat een gebruiker is ingelogd komt deze op het homescherm terecht. Hierop zijn enkele knoppen boven aan het scherm zichtbaar:
1. Home
	Deze knop brengt de gebruiker terug naar het homescherm.

2. Rooster
	Deze knop brengt de gebruiker naar de rooster pagina. Dit is op dit moment nog een stub.

3. Overzicht
	Deze knop brengt de gebruiker naar de overzicht pagina. Hierop is voor een docent te zien welke lessen er voor een bepaald vak zijn ingeplanned.

4. Uitloggen
	Deze knop logt de gebruiker uit.

5. Indien de gebruiker een administrator account gebruikt, is er ook nog de knop Admin
	

# Probleemoplossing:
1. 
```
Foutcode:
File "Pathname here"\venv\Scripts\Activate.ps1 cannot be loaded. The file "Pathname here"\venv\Scripts\Activate.ps1 is not digitally signed. You cannot run this script on the current system. For more information about running scripts and setting execution policy, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.

Oplossing:
Voer de volgende code uit in de terminal: Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process

Waarschuwing!
Dit zorgt ervoor dat elk script in de IDE zonder controle gerunned kan worden, zolang deze draait. Nadat de IDE afgesloten is wordt deze policy weer naar de standaard teruggezet. Zorg er dus voor dat je, als je klaar bent, de IDE afsluit!
```
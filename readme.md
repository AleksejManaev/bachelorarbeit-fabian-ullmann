Bachelorarbeit Fabian Ullmann
========
Fachhochschule Brandenburg <br />
University of Applied Science <br />
Fachbereich Informatik & Medien <br />


Version 0.0.1 - 31.05.2015

by Fabian Ullmann 
<http://ba.20null4.de/>


Introduction
------------
Der aktuelle Entwicklungsstand kann unter <http://ba.20null4.de> betrachtet werden. 

Zur Anmeldung am System stehen folgende User zur Verfügung: 

+ student1 (pass: student1)
+ student2 (pass: student2)
+ tutor2 (pass: tutor1)




Installation and Requirements
-----------------------------

+ PDFTK-Server <https://www.pdflabs.com/tools/pdftk-server/>
+ Python 2.7.10
+ Apache 2.2.2
+ mod_wsgi


+ beautifulsoup4==4.3.2
+ Django==1.8.2
+ django-appconf==1.0.1
+ django-user-accounts==1.0.2
+ fdfgen==0.11.0
+ psycopg2==2.6
+ pytz==2015.4
+ six==1.9.0

### PDFTK-Server ###

Werkzeug für die Manipulation von PDF-Dokumenten.

		apt-get install pdftk


Functions
-------------


### Benutzerfunktionen ###
#### Benutzerkennung ####

Funktionert noch nicht mit LDAP


#### Persönliche Daten ####

+ Nutzer können ihre persönlichen Daten hinterlegen
+ Nutzer können ihre persönlichen Daten ändern

### Absolventenfunktionen ###

#### Praktikum ####

+ Absolventen können Praktikumsarbeit anlegen
+ Absolventen können Praktikum beschreiben
+ Absolventen können Informationen zum Unternehmen erfassen, bei welchem das Praktikum durchgeführt wurde.
+ Absolventen können ihren Praktikumsbericht im System hochladen. 
+ Absolventen können ihr Praktikumszeugnis im System hochladen. 
+ Absolventen können ihre Praktikumspräsentation im System hochladen.

#### Abschlussarbeit ####

+ Absolventen können Abschlussarbeit anlegen
+ Absolventen können die Abschlussarbeit beschreiben
+ Absolventen können Informationen zum Unternehmen erfassen, für welches die Abschlussarbeit durchgeführt wurde.
+ Absolventen können das erfasste Thema einem Dozenten zur Betreuung vorschlagen
+ Absolventen können den Status der Betreuungsanfrage verfolgen 
+ Absolventen können ein vorausgefülltes Anmeldeformular herunterladen


### Gutachterfunktionen ###

#### Betreuungsanfrage ###

+ Gutachter können Anfragen ablehnen
+ Gutachter können Anfragen annehmen 
+ Gutachter können Zweit-Gutachter erfassen


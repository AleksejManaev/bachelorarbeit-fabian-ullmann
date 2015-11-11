Master-Projekt
========
Fachhochschule Brandenburg

University of Applied Science

Fachbereich Informatik & Medien

Allgemeines
------------
Das Projekt setzt die Entwicklung der Bachelorarbeit von Fabian Ullmann fort.
Zu finden unter: <https://bitbucket.org/fhb_fabian/bachelorarbeit-fabian-ullmann/>

Anleitung
---------
Es wird eine teilweise gefüllte Datenbank mitgelifiert.
Ein Student und ein Tutor können sich mit folgenden Zugangsdaten anmelden:
+ student1 : student
+ tutor1 : tutor
+ Email des Tutors: test2@fh-brandenburg.de


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
+ django-bootstrap3
+ django-autofixture

### PDFTK-Server ###

Werkzeug für die Manipulation von PDF-Dokumenten.

		apt-get install pdftk


Funktionen
-------------

### Darstellung ###

+ Für Smartphone, Tablet und Desktop optimiert

### Systemfunktionen ###

+ TODO SSL

### Benutzerfunktionen ###
#### Benutzerkennung ####

+ TODO LDAP-Anbindung


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

+ Absolventen können erhaltene Antwort vom Prüfungsausschuss im System hinterlegen

+ Absolventen können Abschlussarbeit und -Poster hochladen


### Gutachterfunktionen ###

#### Betreuung ####

+ Gutachter können Anfragen ablehnen
+ Gutachter können Anfragen annehmen 
+ Gutachter können Zweit-Gutachter erfassen
+ Gutachter können Erstgespräch festhalten
+ Gutachter können Verlaufsprotokoll pflegen
+ Gutachter können Abgabetermin festlegen

+ Gutachter können erhaltene Antwort vom Prüfungsausschuss im System hinterlegen
+ TODO Gutachter können zu gewünschtem Unternehmen Bewertungen sehen

#### Kolloquium ####

+ Gutachter können Kolloquiumstermin und Uhrzeit festlegen
+ Gutachter können Raum eintragen

- TODO Gutachter können an E-Mail-Verteiler Einladungen zur Teilnhame versenden
- TODO Gutachter können einen vorausgefüllten Begleitbogen für das Kolloquium ausdrucken
- TODO Gutachten können nach gehaltenem Kolloquium die Note eingeben und die Abschlussarbeit abschließen

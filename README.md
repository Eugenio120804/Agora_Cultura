AgoraCultura – Sistema Informativo per Eventi Culturali Locali

AgoraCultura è un sistema informativo web-based progettato per supportare l’organizzazione, la promozione e la partecipazione a eventi culturali locali, offrendo una piattaforma moderna e intuitiva per cittadini, organizzatori e amministratori comunali.

Indice
Obiettivo del Sistema
Tecnologie Utilizzate
Installazione
Configurazione del Database
Utilizzo
Licenza

Obiettivo del Sistema

AgoraCultura nasce con l’obiettivo di:
- 📅 Centralizzare la gestione e la promozione degli eventi culturali del territorio.
- 👥 Facilitare la partecipazione dei cittadini attraverso un’interfaccia semplice e personalizzata.
- 🛠 Consentire agli organizzatori di proporre, modificare e gestire i propri eventi.
- 🧑‍💼 Fornire agli amministratori uno strumento di coordinamento per ruoli, supervisioni e attività.
- 🧾 Archiviare la cronologia degli eventi, recensioni, materiali promozionali e tracciamento delle presenze.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Tecnologie utilizzate
Backend

Python – Linguaggio di programmazione principale.

Django – Framework web per la logica server-side.

mysqlclient – Libreria per collegare Django a MySQL/MariaDB.

Database
MariaDB / MySQL – Database relazionale esterno, gestito tramite phpMyAdmin per facilitare l’inserimento e gestione dei dati.

Frontend
HTML / CSS – Utilizzati per l’interfaccia utente.

Modellazione Dati
Modello E/R progettato con generalizzazioni disgiunte e totali, garantendo una struttura dati coerente e scalabile.
![AgoraCultura drawio](https://github.com/user-attachments/assets/67c97d27-171c-472c-a1e0-946875757b26)

Per eseguire l’applicazione, è necessario:

1. Avere Python installato nel proprio ambiente.
2. Avere accesso a un server MySQL/MariaDB, preferibilmente con phpMyAdmin.
3. Clonare il progetto nella propria directory locale.

git clone https://github.com/Eugenio120804/Agora_Cultura.git
cd Agora_Cultura

4. Creare e attivare un ambiente virtuale (consigliato)
python -m venv venv

Linux/macOS
source venv/bin/activate

Windows
In cmd
venv\Scripts\activate.bat

In PowerShell
.\venv\Scripts\Activate.ps1

5. Installare le dipendenze
pip install -r requirements.txt

Se non si vuole usare il file requirements.txt, installare manualmente eseguendo:
pip install django mysqlclient

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Configurazione del Database
Importare il database da dump SQL* Se disponi di un file .sql con il dump del database puoi importarlo nel tuo server MySQL/MariaDB.
Metodo 1: via phpMyAdmin

Accedi a phpMyAdmin
Crea un nuovo database
Clicca su Importa e carica il file dump.sql
Configurazione Database su Django All’interno del file settings.py del progetto Django, è necessario configurare correttamente la connessione al database MySQL/MariaDB. I parametri da inserire sono:

DATABASES = {

    'default': 
    
        'ENGINE': 'django.db.backends.mysql',
        
        'NAME': 'nome_database',
        
        'USER': 'nome_utente',
        
        'PASSWORD': ‘ ’,
        
        'HOST': 'localhost',
        
        'PORT': '3306',
    }
}


Utilizzo

Dopo la configurazione, eseguire i seguenti comandi da terminale per applicare le migrazioni:

python manage.py makemigrations
python manage.py migrate
Una volta completato, si può avviare il server locale con:

manage.py runserver

L'applicazione sarà accessibile all'indirizzo: http://localhost:8000.
![image](https://github.com/user-attachments/assets/44e11b09-3932-4481-9640-3139fd480211)

Contenuti principali:
•	Presentazione della piattaforma: messaggio di benvenuto che introduce l’obiettivo del portale: facilitare l’accesso e la partecipazione ad eventi culturali locali.
•	Accesso Area Riservata: pulsanti che indirizzano l’utente verso il login o la registrazione.
•	Calendario Eventi: accesso rapido alla sezione contenente il calendario completo degli eventi disponibili.
•	Recensioni e Area Personale: indicazioni sulle funzionalità riservate agli utenti autenticati, come lasciare recensioni e consultare lo storico personale.

Area riservata – Gestione Autenticata (con sessioni)

La piattaforma integra il sistema di autenticazione e gestione delle sessioni di Django, differenziando i permessi in base al ruolo dell’utente. I pazienti possono registrarsi autonomamente creando un account personale tramite un modulo dedicato. Successivamente possono effettuare il login per accedere alle funzionalità riservate.
L’organizzatore e l’amministratore comunale accede solo tramite login, con credenziali già definite e riportate nel database.

Login Cittadino

L’utente cittadino ha accesso a un’area personale dedicata, con funzionalità mirate all’esperienza culturale:
•	Visualizzazione calendario eventi: può esplorare eventi culturali, visionare orari e dettagli.
•	Inserimento recensioni: può lasciare recensioni per eventi a cui ha partecipato.
•	Storico recensioni: consultazione e gestione delle recensioni già inserite.
 
Login Organizzatore

L’organizzatore ha accesso a strumenti di gestione degli eventi:
•	Proposta nuovi eventi: possibilità di creare e proporre un nuovo evento culturale.
•	Modifica eventi esistenti: può aggiornare titolo, descrizione, luogo e data degli eventi proposti.
 
Login Amministratore

L’amministratore ha accesso completo alle funzioni di supervisione e controllo qualità:
•	Supervisione eventi: può supervisionare eventi organizzati da utenti con ruolo “Organizzatore”.
•	Evidenziazione eventi: può contrassegnare un evento come "in evidenza" solo se è stato effettivamente supervisionato.
 
Cittadino
![image](https://github.com/user-attachments/assets/3456f905-1b1c-4516-9b13-3f1cf9392da5)

Organizzatore
![image](https://github.com/user-attachments/assets/255af1d1-5b4d-4df2-a691-65f8cfd6c83d)

Amministratore
![image](https://github.com/user-attachments/assets/c7d62eae-ad4b-416f-94eb-4d58b4f6ad75)

Licenza
Questo progetto è stato realizzato e distribuito a scopo didattico con licenza MIT. Puoi usarlo, modificarlo e distribuirlo liberamente, a patto che venga mantenuta la nota di copyright.





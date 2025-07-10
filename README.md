
# AgoraCultura – Sistema Informativo per Eventi Culturali Locali

**AgoraCultura** è un sistema informativo web-based progettato per supportare l’organizzazione, la promozione e la partecipazione a eventi culturali locali, offrendo una piattaforma moderna e intuitiva per cittadini, organizzatori e amministratori comunali.

---

## 📑 Indice

- [Obiettivo del Sistema](#obiettivo-del-sistema)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Installazione](#installazione)
- [Configurazione del Database](#configurazione-del-database)
- [Utilizzo](#utilizzo)
- [Licenza](#licenza)

---

## 🎯 Obiettivo del Sistema

AgoraCultura nasce con l’obiettivo di:

- Centralizzare la gestione e la promozione degli eventi culturali del territorio.
- Facilitare la partecipazione dei cittadini attraverso un’interfaccia semplice e personalizzata.
- Consentire agli organizzatori di proporre, modificare e gestire i propri eventi.
- Fornire agli amministratori uno strumento di coordinamento per ruoli, supervisioni e attività.
- Archiviare la cronologia degli eventi, recensioni, materiali promozionali e tracciamento delle presenze.

---

## 🧰 Tecnologie Utilizzate

### Backend
- **Python** – Linguaggio di programmazione principale
- **Django** – Framework web
- **mysqlclient** – Libreria per connettere Django a MySQL/MariaDB

### Database
- **MariaDB / MySQL** – Gestito via **phpMyAdmin**

### Frontend
- **HTML / CSS** – Per la realizzazione dell’interfaccia utente

### Modellazione Dati
- **Modello E/R** con generalizzazioni disgiunte e totali, garantendo coerenza e scalabilità

![Modello ER](https://github.com/user-attachments/assets/67c97d27-171c-472c-a1e0-946875757b26)

---

## ⚙️ Installazione

Per eseguire l’applicazione:

1. Assicurati di avere **Python** installato.

2. Avere accesso a un server **MySQL/MariaDB**, preferibilmente con **phpMyAdmin**.

3. Clona il repository:
   ```bash
   git clone https://github.com/Eugenio120804/Agora_Cultura.git
   cd Agora_Cultura
   ```

4. Crea e attiva un ambiente virtuale:
   ```bash
   python -m venv venv
   ```

   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```

   - **Windows CMD**:
     ```cmd
     venv\Scripts\activate.bat
     ```

   - **Windows PowerShell**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

5. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

   Oppure manualmente:
   ```bash
   pip install django mysqlclient
   ```

---

## 🛠️ Configurazione del Database

### Importazione tramite phpMyAdmin

1. Accedi a **phpMyAdmin**
2. Crea un nuovo database
3. Clicca su **Importa** e carica il file `dump.sql`

### Configurazione in Django

Modifica la sezione `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_database',
        'USER': 'nome_utente',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 🚀 Utilizzo

Esegui le migrazioni:
```bash
python manage.py makemigrations
python manage.py migrate
```

Avvia il server locale:
```bash
python manage.py runserver
```

Apri nel browser: [http://localhost:8000](http://localhost:8000)

### Contenuti principali

- **Presentazione piattaforma**: messaggio di benvenuto
- **Accesso Area Riservata**: login e registrazione
- **Calendario Eventi**
- **Recensioni e Area Personale**

### Area Riservata – Gestione Autenticata

Gestione sessioni con login differenziato in base al ruolo:

---

#### 👤 Login Cittadino

- Visualizzazione calendario eventi
- Inserimento recensioni
- Storico recensioni

![Cittadino](https://github.com/user-attachments/assets/3456f905-1b1c-4516-9b13-3f1cf9392da5)

---

#### 📝 Login Organizzatore

- Proposta nuovi eventi
- Modifica eventi esistenti

![Organizzatore](https://github.com/user-attachments/assets/255af1d1-5b4d-4df2-a691-65f8cfd6c83d)

---

#### 🛡️ Login Amministratore

- Supervisione eventi
- Evidenziazione eventi

![Amministratore](https://github.com/user-attachments/assets/c7d62eae-ad4b-416f-94eb-4d58b4f6ad75)

---

## 📄 Licenza

Questo progetto è distribuito sotto **Licenza MIT**.  
Puoi usarlo, modificarlo e distribuirlo liberamente, a condizione che venga mantenuto il copyright.

---

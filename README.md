🏛️ Agora Cultura
Piattaforma per la gestione e promozione di eventi culturali, con funzionalità per prenotazioni, recensioni, categorizzazione eventi e ruoli utenti differenziati.

📚 Informazioni generali
Agora Cultura è un'applicazione web sviluppata con Django, progettata per supportare l’organizzazione e la partecipazione a eventi culturali locali. 
Il sistema permette a cittadini, organizzatori e amministratori di interagire in modo sicuro e strutturato attraverso funzionalità come:

- Registrazione e autenticazione utenti
- Proposta e supervisione di eventi
- Prenotazione posti (gratuiti o a pagamento)
- Inserimento recensioni post-evento
- Categorizzazione e promozione eventi in evidenza
- Gerarchia e supervisione tra utenti

🚀 Istruzioni per l’avvio del progetto
1. Clona il repository
git clone https://github.com/Eugenio120804/Agora_Cultura.git
cd Agora_Cultura

2. Crea e attiva un ambiente virtuale
python -m venv env
source env/bin/activate  # Su Windows: env\Scripts\activate

3. Installa le dipendenze
pip install -r requirements.txt

4. Applica le migrazioni
python manage.py migrate

5. Avvia il server di sviluppo
python manage.py runserver

6. Crea un superutente per l’accesso all’admin
python manage.py createsuperuser


👤 Autore
Eugenio120804

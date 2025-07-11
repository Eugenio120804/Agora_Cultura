from django.core.management.base import BaseCommand
import hashlib
from django.utils import timezone
from AgoraCultura.models import Utente, Luogo, Categoria, Evento, Svolgimento, Prenotazione, Recensione, Supervisione, Associazione
from decimal import Decimal
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Popola il database con dati di esempio'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Inizializzazione popolamento database...'))

        # Creazione utenti
        self.create_users()

        # Creazione luoghi (con Marigliano come città)
        self.create_locations()

        # Creazione categorie
        self.create_categories()

        # Associazione eventi a categorie
        self.associate_events_categories()

        # Creazione svolgimenti (collegamento eventi a luoghi)
        self.create_performances()

        # Creazione prenotazioni
        self.create_bookings()

        # Creazione recensioni
        self.create_reviews()

        # Creazione supervisioni
        self.create_supervisions()

        self.stdout.write(self.style.SUCCESS('Popolamento database completato con successo!'))

    def create_users(self):
        # Definizione utenti
        users = [
            {
                'username': 'cittadino1',
                'password': 'password123',
                'email': 'cittadino1@example.com',
                'first_name': 'Mario',
                'last_name': 'Rossi',
                'ruolo': 'Cittadino'
            },
            {
                'username': 'cittadino2',
                'password': 'password123',
                'email': 'cittadino2@example.com',
                'first_name': 'Laura',
                'last_name': 'Bianchi',
                'ruolo': 'Cittadino'
            },
            {
                'username': 'organizzatore1',
                'password': 'password123',
                'email': 'organizzatore1@example.com',
                'first_name': 'Giuseppe',
                'last_name': 'Verdi',
                'ruolo': 'Organizzatore'
            },
            {
                'username': 'organizzatore2',
                'password': 'password123',
                'email': 'organizzatore2@example.com',
                'first_name': 'Francesca',
                'last_name': 'Neri',
                'ruolo': 'Organizzatore'
            },
            {
                'username': 'admin1',
                'password': 'password123',
                'email': 'admin1@example.com',
                'first_name': 'Antonio',
                'last_name': 'Esposito',
                'ruolo': 'Amministratore'
            }
        ]

        created = 0
        existing = 0

        for user_data in users:
            if not Utente.objects.filter(username=user_data['username']).exists():
                # Hash della password con MD5
                password_md5 = hashlib.md5(user_data['password'].encode()).hexdigest()
                Utente.objects.create(
                    username=user_data['username'],
                    password=password_md5,
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    ruolo=user_data['ruolo']
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Utente creato: {user_data["username"]}'))
            else:
                existing += 1
                self.stdout.write(self.style.WARNING(f'Utente già esistente: {user_data["username"]}'))

        self.stdout.write(self.style.SUCCESS(f'Creazione utenti completata: {created} creati, {existing} già esistenti.'))

    def create_locations(self):
        # Definizione luoghi (tutti con città Marigliano come richiesto)
        locations = [
            {
                'nome': 'Teatro Comunale',
                'indirizzo': 'Via Roma 123',
                'capienza': 300,
                'citta': 'Marigliano'
            },
            {
                'nome': 'Piazza Centrale',
                'indirizzo': 'Piazza Municipio',
                'capienza': 1000,
                'citta': 'Marigliano'
            },
            {
                'nome': 'Biblioteca Civica',
                'indirizzo': 'Corso Italia 45',
                'capienza': 150,
                'citta': 'Marigliano'
            },
            {
                'nome': 'Parco Pubblico',
                'indirizzo': 'Via dei Pini 78',
                'capienza': 500,
                'citta': 'Marigliano'
            },
            {
                'nome': 'Centro Culturale',
                'indirizzo': 'Via Napoli 22',
                'capienza': 200,
                'citta': 'Marigliano'
            }
        ]

        created = 0
        existing = 0

        for location_data in locations:
            if not Luogo.objects.filter(nome=location_data['nome'], citta=location_data['citta']).exists():
                Luogo.objects.create(
                    nome=location_data['nome'],
                    indirizzo=location_data['indirizzo'],
                    capienza=location_data['capienza'],
                    citta=location_data['citta']
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Luogo creato: {location_data["nome"]} - {location_data["citta"]}'))
            else:
                existing += 1
                self.stdout.write(self.style.WARNING(f'Luogo già esistente: {location_data["nome"]} - {location_data["citta"]}'))

        self.stdout.write(self.style.SUCCESS(f'Creazione luoghi completata: {created} creati, {existing} già esistenti.'))

    def create_categories(self):
        # Definizione categorie
        categories = [
            'Musica',
            'Arte',
            'Teatro',
            'Letteratura',
            'Cinema',
            'Danza',
            'Fotografia',
            'Gastronomia',
            'Storia',
            'Scienza'
        ]

        created = 0
        existing = 0

        for category_name in categories:
            if not Categoria.objects.filter(nome=category_name).exists():
                Categoria.objects.create(nome=category_name)
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Categoria creata: {category_name}'))
            else:
                existing += 1
                self.stdout.write(self.style.WARNING(f'Categoria già esistente: {category_name}'))

        self.stdout.write(self.style.SUCCESS(f'Creazione categorie completata: {created} create, {existing} già esistenti.'))

    def associate_events_categories(self):
        # Associazione eventi a categorie
        eventi = Evento.objects.all()
        categorie = Categoria.objects.all()

        if not eventi:
            self.stdout.write(self.style.WARNING('Nessun evento trovato. Esegui prima il comando populate_events.'))
            return

        if not categorie:
            self.stdout.write(self.style.WARNING('Nessuna categoria trovata.'))
            return

        created = 0
        existing = 0

        for evento in eventi:
            # Assegna 1-3 categorie casuali a ogni evento
            num_categorie = random.randint(1, 3)
            categorie_casuali = random.sample(list(categorie), min(num_categorie, len(categorie)))

            for categoria in categorie_casuali:
                if not Associazione.objects.filter(evento=evento, categoria=categoria).exists():
                    Associazione.objects.create(evento=evento, categoria=categoria)
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'Associazione creata: {evento.titolo} - {categoria.nome}'))
                else:
                    existing += 1
                    self.stdout.write(self.style.WARNING(f'Associazione già esistente: {evento.titolo} - {categoria.nome}'))

        self.stdout.write(self.style.SUCCESS(f'Associazione eventi-categorie completata: {created} create, {existing} già esistenti.'))

    def create_performances(self):
        # Creazione svolgimenti (collegamento eventi a luoghi)
        eventi = Evento.objects.all()
        luoghi = Luogo.objects.all()

        if not eventi:
            self.stdout.write(self.style.WARNING('Nessun evento trovato. Esegui prima il comando populate_events.'))
            return

        if not luoghi:
            self.stdout.write(self.style.WARNING('Nessun luogo trovato.'))
            return

        created = 0
        existing = 0

        # Data di partenza per gli eventi (oggi)
        start_date = timezone.now().date()

        for evento in eventi:
            # Crea 1-3 svolgimenti per ogni evento
            num_svolgimenti = random.randint(1, 3)

            for i in range(num_svolgimenti):
                # Scegli un luogo casuale
                luogo = random.choice(luoghi)

                # Genera una data casuale nei prossimi 60 giorni
                random_days = random.randint(1, 60)
                data = start_date + timedelta(days=random_days)

                # Genera un orario casuale tra le 10:00 e le 22:00
                hour = random.randint(10, 22)
                minute = random.choice([0, 15, 30, 45])
                orario = f"{hour:02d}:{minute:02d}"

                # Verifica se lo svolgimento esiste già
                if not Svolgimento.objects.filter(evento=evento, luogo=luogo, data=data, orario=orario).exists():
                    Svolgimento.objects.create(
                        evento=evento,
                        luogo=luogo,
                        data=data,
                        orario=orario,
                        videoprime=None if random.random() > 0.3 else f"https://example.com/video/{evento.id}_{i}"
                    )
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'Svolgimento creato: {evento.titolo} - {luogo.nome} - {data} {orario}'))
                else:
                    existing += 1
                    self.stdout.write(self.style.WARNING(f'Svolgimento già esistente: {evento.titolo} - {luogo.nome} - {data} {orario}'))

        self.stdout.write(self.style.SUCCESS(f'Creazione svolgimenti completata: {created} creati, {existing} già esistenti.'))

    def create_bookings(self):
        # Creazione prenotazioni
        utenti = Utente.objects.filter(ruolo='Cittadino')
        eventi = Evento.objects.all()

        if not utenti:
            self.stdout.write(self.style.WARNING('Nessun utente cittadino trovato.'))
            return

        if not eventi:
            self.stdout.write(self.style.WARNING('Nessun evento trovato.'))
            return

        created = 0
        existing = 0

        for utente in utenti:
            # Crea 1-5 prenotazioni per ogni utente
            num_prenotazioni = random.randint(1, 5)
            eventi_casuali = random.sample(list(eventi), min(num_prenotazioni, len(eventi)))

            for evento in eventi_casuali:
                if not Prenotazione.objects.filter(utente=utente, evento=evento).exists():
                    stato = random.choice(['Confermata', 'Confermata', 'Confermata', 'Annullata'])  # 75% confermate, 25% annullate
                    Prenotazione.objects.create(
                        utente=utente,
                        evento=evento,
                        stato=stato
                    )
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'Prenotazione creata: {utente.username} - {evento.titolo} - {stato}'))
                else:
                    existing += 1
                    self.stdout.write(self.style.WARNING(f'Prenotazione già esistente: {utente.username} - {evento.titolo}'))

        self.stdout.write(self.style.SUCCESS(f'Creazione prenotazioni completata: {created} create, {existing} già esistenti.'))

    def create_reviews(self):
        # Creazione recensioni
        prenotazioni = Prenotazione.objects.filter(stato='Confermata')

        if not prenotazioni:
            self.stdout.write(self.style.WARNING('Nessuna prenotazione confermata trovata.'))
            return

        created = 0
        existing = 0

        for prenotazione in prenotazioni:
            # Solo il 70% delle prenotazioni confermate ha una recensione
            if random.random() <= 0.7:
                if not Recensione.objects.filter(utente=prenotazione.utente, evento=prenotazione.evento).exists():
                    valutazione = random.randint(1, 5)
                    testi_recensione = [
                        "Ottimo evento, lo consiglio vivamente!",
                        "Esperienza interessante, ma migliorabile in alcuni aspetti.",
                        "Buona organizzazione e contenuti di qualità.",
                        "Un'esperienza culturale arricchente.",
                        "Evento ben strutturato, ma location non ideale.",
                        "Contenuti eccellenti, ma durata eccessiva.",
                        "Superato le mie aspettative, tornerò sicuramente!",
                        "Interessante ma non eccezionale.",
                        "Ottimo rapporto qualità-prezzo.",
                        "Un'esperienza unica nel suo genere."
                    ]
                    testo = random.choice(testi_recensione)

                    Recensione.objects.create(
                        utente=prenotazione.utente,
                        evento=prenotazione.evento,
                        testo=testo,
                        valutazione=valutazione
                    )
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'Recensione creata: {prenotazione.utente.username} - {prenotazione.evento.titolo} - {valutazione}/5'))
                else:
                    existing += 1
                    self.stdout.write(self.style.WARNING(f'Recensione già esistente: {prenotazione.utente.username} - {prenotazione.evento.titolo}'))

        self.stdout.write(self.style.SUCCESS(f'Creazione recensioni completata: {created} create, {existing} già esistenti.'))

    def create_supervisions(self):
        # Creazione supervisioni (amministratori supervisionano organizzatori)
        amministratori = Utente.objects.filter(ruolo='Amministratore')
        organizzatori = Utente.objects.filter(ruolo='Organizzatore')

        if not amministratori:
            self.stdout.write(self.style.WARNING('Nessun amministratore trovato.'))
            return

        if not organizzatori:
            self.stdout.write(self.style.WARNING('Nessun organizzatore trovato.'))
            return

        created = 0
        existing = 0

        for amministratore in amministratori:
            for organizzatore in organizzatori:
                if not Supervisione.objects.filter(supervisore=amministratore, supervisionato=organizzatore).exists():
                    Supervisione.objects.create(
                        supervisore=amministratore,
                        supervisionato=organizzatore
                    )
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'Supervisione creata: {amministratore.username} supervisiona {organizzatore.username}'))
                else:
                    existing += 1
                    self.stdout.write(self.style.WARNING(f'Supervisione già esistente: {amministratore.username} - {organizzatore.username}'))

        self.stdout.write(self.style.SUCCESS(f'Creazione supervisioni completata: {created} create, {existing} già esistenti.'))

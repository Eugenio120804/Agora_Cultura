from django.core.management.base import BaseCommand
from AgoraCultura.models import Evento
from decimal import Decimal

class Command(BaseCommand):
    help = 'Popola il database con 10 eventi predefiniti'

    def handle(self, *args, **kwargs):
        # Lista degli eventi da creare
        eventi = [
            {
                'titolo': 'Notte Jazz sotto le Stelle',
                'descrizione': 'Concerto all\'aperto con artisti jazz internazionali nel centro storico.',
                'prezzo': Decimal('25.00'),
                'tipologia': 'Concerto',
                'evidenza': True
            },
            {
                'titolo': 'Mostra "Colori dell\'Anima"',
                'descrizione': 'Esposizione di opere astratte di giovani artisti emergenti.',
                'prezzo': Decimal('12.00'),
                'tipologia': 'Mostra',
                'evidenza': False
            },
            {
                'titolo': 'Laboratorio di Ceramica per Principianti',
                'descrizione': 'Attività pratica per imparare le basi della modellazione dell\'argilla.',
                'prezzo': Decimal('18.00'),
                'tipologia': 'Laboratorio',
                'evidenza': False
            },
            {
                'titolo': 'Spettacolo "Il Giardino dei Segreti"',
                'descrizione': 'Rappresentazione teatrale tratto dal romanzo classico per famiglie.',
                'prezzo': Decimal('20.00'),
                'tipologia': 'Spettacolo teatrale',
                'evidenza': True
            },
            {
                'titolo': 'Conferenza "Intelligenza Artificiale & Etica"',
                'descrizione': 'Esperti discutono delle sfide etiche legate all\'IA.',
                'prezzo': Decimal('10.00'),
                'tipologia': 'Conferenza',
                'evidenza': False
            },
            {
                'titolo': 'Festival della Letteratura Mediterranea',
                'descrizione': 'Incontri con autori, letture pubbliche e dibattiti culturali.',
                'prezzo': Decimal('15.00'),
                'tipologia': 'Conferenza',
                'evidenza': True
            },
            {
                'titolo': 'Concerto Acustico al Tramonto',
                'descrizione': 'Performance musicale unplugged in riva al lago.',
                'prezzo': Decimal('8.50'),
                'tipologia': 'Concerto',
                'evidenza': False
            },
            {
                'titolo': 'Mostra Fotografica "Sguardi nel Tempo"',
                'descrizione': 'Ritratti in bianco e nero che raccontano la vita nelle campagne italiane.',
                'prezzo': Decimal('6.00'),
                'tipologia': 'Mostra',
                'evidenza': False
            },
            {
                'titolo': 'Spettacolo "Comici per una Notte"',
                'descrizione': 'Serata di cabaret con artisti locali e ospiti speciali.',
                'prezzo': Decimal('14.00'),
                'tipologia': 'Spettacolo teatrale',
                'evidenza': True
            },
            {
                'titolo': 'Laboratorio di Scrittura Creativa',
                'descrizione': 'Corso breve per sviluppare tecniche narrative e storytelling.',
                'prezzo': Decimal('22.00'),
                'tipologia': 'Laboratorio',
                'evidenza': False
            }
        ]

        # Contatori per il report finale
        creati = 0
        esistenti = 0

        # Creazione degli eventi
        for evento_data in eventi:
            # Verifica se l'evento esiste già (basandosi sul titolo)
            if not Evento.objects.filter(titolo=evento_data['titolo']).exists():
                Evento.objects.create(
                    titolo=evento_data['titolo'],
                    descrizione=evento_data['descrizione'],
                    prezzo=evento_data['prezzo'],
                    tipologia=evento_data['tipologia'],
                    evidenza=evento_data['evidenza']
                )
                creati += 1
                self.stdout.write(self.style.SUCCESS(f'Evento creato: {evento_data["titolo"]}'))
            else:
                esistenti += 1
                self.stdout.write(self.style.WARNING(f'Evento già esistente: {evento_data["titolo"]}'))

        # Report finale
        self.stdout.write(self.style.SUCCESS(f'Popolamento completato: {creati} eventi creati, {esistenti} eventi già esistenti.'))
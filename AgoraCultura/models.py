from django.contrib.auth.models import AbstractUser
from django.db import models

class Utente(AbstractUser):
    RUOLI = (
        ('Cittadino', 'Cittadino'),
        ('Organizzatore', 'Organizzatore'),
        ('Amministratore', 'Amministratore'),
    )
    ruolo = models.CharField(max_length=20, choices=RUOLI)

class Luogo(models.Model):
    nome = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=255)
    capienza = models.IntegerField()
    citta = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.citta}"

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    prezzo = models.DecimalField(max_digits=6, decimal_places=2)
    tipologia = models.CharField(max_length=100)
    evidenza = models.BooleanField(default=False)
    supervisionato = models.BooleanField(default=False)
    organizzatore = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='eventi_organizzati', null=True)
    categorie = models.ManyToManyField(Categoria, through='Associazione')

    def __str__(self):
        return self.titolo

class Svolgimento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    luogo = models.ForeignKey(Luogo, on_delete=models.CASCADE)
    data = models.DateField()
    orario = models.TimeField()
    videoprime = models.URLField(blank=True, null=True)

class Prenotazione(models.Model):
    STATO_CHOICES = (
        ('Confermata', 'Confermata'),
        ('Annullata', 'Annullata'),
    )
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_prenotazione = models.DateField(auto_now_add=True)
    stato = models.CharField(max_length=20, choices=STATO_CHOICES)

    class Meta:
        unique_together = ('utente', 'evento')

class Recensione(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    testo = models.TextField()
    valutazione = models.IntegerField()
    data = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('utente', 'evento')

class Supervisione(models.Model):
    supervisore = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='supervisore')
    supervisionato = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='supervisionato')

    class Meta:
        unique_together = ('supervisore', 'supervisionato')

class Associazione(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('evento', 'categoria')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utente, Recensione

class RegistrazioneForm(UserCreationForm):
    class Meta:
        model = Utente
        fields = ['username', 'email', 'password1', 'password2', 'ruolo']
        labels = {
            'username': 'Nome utente',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Conferma Password',
            'ruolo': 'Ruolo',
        }

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['testo', 'valutazione']
        labels = {
            'testo': 'Scrivi una recensione',
            'valutazione': 'Valutazione (1-5)',
        }
        widgets = {
            'testo': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'valutazione': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
        }


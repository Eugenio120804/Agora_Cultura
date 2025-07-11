from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utente, Recensione, Evento, Categoria, Svolgimento, Luogo
import hashlib

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Include solo l'opzione Cittadino
        self.fields['ruolo'].choices = [('Cittadino', 'Cittadino')]
        self.fields['ruolo'].initial = 'Cittadino'
        self.fields['ruolo'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        user = self.instance
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.ruolo = self.cleaned_data.get('ruolo')

        # Hash della password con MD5
        password = self.cleaned_data.get('password1')
        user.password = hashlib.md5(password.encode()).hexdigest()

        if commit:
            user.save()
        return user

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

    def clean_valutazione(self):
        valutazione = self.cleaned_data.get('valutazione')
        if valutazione is not None and (valutazione < 1 or valutazione > 5):
            raise forms.ValidationError("La valutazione deve essere compresa tra 1 e 5.")
        return valutazione

class EventoForm(forms.ModelForm):
    categorie = forms.ModelMultipleChoiceField(
        queryset = Categoria.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Categorie'
    )

class EventoFormOrganizzatore(EventoForm):

    class Meta:
        model = Evento
        fields = ['titolo', 'descrizione', 'prezzo', 'tipologia', 'categorie']
        labels = {
            'titolo': 'Titolo',
            'descrizione': 'Descrizione',
            'prezzo': 'Prezzo',
            'tipologia': 'Tipologia',
            'evidenza': 'In evidenza',
        }
        widgets = {
            'descrizione': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'prezzo': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'tipologia': forms.TextInput(attrs={'class': 'form-control'}),
            'evidenza': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_evidenza(self):
        evidenza = self.cleaned_data.get('evidenza')

        # Se l'evento è in evidenza, verifichiamo che sia stato supervisionato
        if evidenza:
            # Se è un nuovo evento, non può essere in evidenza
            if not self.instance.pk:
                raise forms.ValidationError("Un nuovo evento non può essere messo in evidenza prima di essere supervisionato.")

            # Se è un evento esistente, verifichiamo che sia stato supervisionato
            if not self.instance.supervisionato:
                raise forms.ValidationError("Solo gli eventi supervisionati possono essere messi in evidenza.")

        return evidenza

class SvolgimentoForm(forms.ModelForm):
    class Meta:
        model = Svolgimento
        fields = ['luogo', 'data', 'orario']
        labels = {
            'luogo': 'Luogo',
            'data': 'Data',
            'orario': 'Orario',
        }
        widgets = {
            'luogo': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'orario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

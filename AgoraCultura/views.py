from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Evento, Svolgimento, Recensione, Prenotazione
from .forms import RegistrazioneForm, RecensioneForm

def home(request):
    return render(request, 'home.html')

def dettaglio_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    recensioni = Recensione.objects.filter(evento=evento)
    return render(request, 'dettaglio_evento.html', {
        'evento': evento,
        'recensioni': recensioni
    })

def registrazione(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrazioneForm()
    return render(request, 'register.html', {'form': form})

@login_required
def lascia_recensione(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        form = RecensioneForm(request.POST)
        if form.is_valid():
            recensione = form.save(commit=False)
            recensione.utente = request.user
            recensione.evento = evento
            recensione.save()
            return redirect('dettaglio_evento', evento_id=evento_id)
    else:
        form = RecensioneForm()
    return render(request, 'recensione_evento.html', {'form': form, 'evento': evento})

@login_required
def area_personale(request):
    prenotazioni = Prenotazione.objects.filter(utente=request.user)
    eventi_partecipati = [p.evento for p in prenotazioni]
    return render(request, 'area_personale.html', {
        'eventi_partecipati': eventi_partecipati
    })

@login_required
def calendario_eventi(request):
    eventi = Evento.objects.all().order_by('data')
    return render(request, 'calendario_eventi.html', {'eventi': eventi})

from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Username o password errati.'})
    return render(request, 'login.html')


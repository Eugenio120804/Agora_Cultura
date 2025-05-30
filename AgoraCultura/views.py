from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Evento, Svolgimento, Recensione, Prenotazione
from .forms import RegistrazioneForm, RecensioneForm

def home(request):
    return render(request, 'home.html')

def dettaglio_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    svolgimenti = Svolgimento.objects.filter(evento=evento).order_by('data', 'orario')
    recensioni = Recensione.objects.filter(evento=evento)
    return render(request, 'dettaglio_evento.html', {
        'evento': evento,
        'svolgimenti': svolgimenti,
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
    prenotazioni = Prenotazione.objects.filter(utente=request.user).select_related('evento')
    recensioni = Recensione.objects.filter(utente=request.user).select_related('evento')

    # Get the first upcoming svolgimento for each event
    eventi_info = []
    for prenotazione in prenotazioni:
        evento = prenotazione.evento
        svolgimento = Svolgimento.objects.filter(evento=evento, data__gte=prenotazione.data_prenotazione).order_by('data', 'orario').first()
        if svolgimento:
            eventi_info.append({
                'evento': evento,
                'prenotazione': prenotazione,
                'svolgimento': svolgimento
            })

    return render(request, 'area_personale.html', {
        'eventi_info': eventi_info,
        'recensioni': recensioni,
        'user': request.user
    })

def calendario_eventi(request):
    svolgimenti = Svolgimento.objects.all().order_by('data', 'orario')
    return render(request, 'calendario_eventi.html', {'svolgimenti': svolgimenti})

from django.contrib.auth import login

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from .models import Evento, Svolgimento, Recensione, Prenotazione, Associazione, Utente
from .forms import RegistrazioneForm, RecensioneForm, EventoForm, EventoFormOrganizzatore, SvolgimentoForm
from django.contrib.auth import login
import hashlib
from django.db import connection
from django.http import HttpResponse


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            # Convert single role to list for uniform handling
            required_roles = [roles] if isinstance(roles, str) else roles

            # Check if the user has the required role
            if request.user.ruolo in required_roles:
                # Check if the appropriate session variable exists based on the user's role
                if request.user.ruolo == 'Cittadino' and 'cittadino_email' not in request.session:
                    return redirect('login')
                elif request.user.ruolo == 'Organizzatore' and 'organizzatore_email' not in request.session:
                    return redirect('login')
                elif request.user.ruolo == 'Amministratore' and 'amministratore_email' not in request.session:
                    return redirect('login')

                # If the user has the required role and the appropriate session variable exists, allow access
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden(f"Accesso negato. Ruolo richiesto: {', '.join(required_roles)}")
        return _wrapped_view
    return decorator

def home(request):
    # Se l'utente è autenticato e ha il ruolo di Organizzatore o Amministratore
    if request.user.is_authenticated:
        if request.user.ruolo == 'Organizzatore' and 'organizzatore_email' not in request.session:
            return redirect('login')
        elif request.user.ruolo == 'Amministratore' and 'amministratore_email' not in request.session:
            return redirect('login')

    return render(request, 'home.html')

def dettaglio_evento(request, evento_id):
    # Se l'utente è autenticato e ha il ruolo di Organizzatore o Amministratore
    if request.user.is_authenticated:
        if request.user.ruolo == 'Organizzatore' and 'organizzatore_email' not in request.session:
            return redirect('login')
        elif request.user.ruolo == 'Amministratore' and 'amministratore_email' not in request.session:
            return redirect('login')

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
            # Ensure that only citizens can register
            form.instance.ruolo = 'Cittadino'
            user = form.save()
            login(request, user)

            # Set the session variable for citizen
            request.session['cittadino_email'] = user.email

            return redirect('home')
    else:
        form = RegistrazioneForm()
    return render(request, 'register.html', {'form': form})

@role_required(['Cittadino', 'Amministratore'])
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

    eventi_organizzatore = []
    if request.user.ruolo == 'Organizzatore':
        eventi_organizzatore = Evento.objects.all()

    return render(request, 'area_personale.html', {
        'eventi_info': eventi_info,
        'recensioni': recensioni,
        'eventi_organizzatore': eventi_organizzatore,
        'user': request.user
    })

def calendario_eventi(request):
    # Se l'utente è autenticato e ha il ruolo di Organizzatore o Amministratore
    if request.user.is_authenticated:
        if request.user.ruolo == 'Organizzatore' and 'organizzatore_email' not in request.session:
            return redirect('login')
        elif request.user.ruolo == 'Amministratore' and 'amministratore_email' not in request.session:
            return redirect('login')

    svolgimenti = Svolgimento.objects.all().order_by('data', 'orario')
    return render(request, 'calendario_eventi.html', {'svolgimenti': svolgimenti})


def autenticazione_cittadino(email, password):
    try:
        user = Utente.objects.get(email=email, ruolo='Cittadino')
        password_md5 = hashlib.md5(password.encode()).hexdigest()
        if password_md5 == user.password:
            return user
    except Utente.DoesNotExist:
        pass
    return None


# Funzione vulnerabile a SQL injection
def autenticazione_vulnerabile(username, password):
    with connection.cursor() as cursor:
        # Query vulnerabile: concatena direttamente l'input dell'utente
        query = f"SELECT * FROM AgoraCultura_utente WHERE username = '{username}' AND password = '{hashlib.md5(password.encode()).hexdigest()}'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            # Crea un oggetto Utente dai risultati della query
            user_id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, ruolo = result
            user = Utente(
                id=user_id,
                username=username,
                password=password,
                email=email,
                ruolo=ruolo
            )
            return user
    return None


def login_cittadino(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # L'email viene inserita nel campo username
        password = request.POST.get('password')
        user = autenticazione_cittadino(email, password)

        # Se esiste un cittadino con email e password corrispondenti
        if user is not None:
            # Crea una sessione per l'utente inserendo l'email nella chiave 'cittadino_email'
            login(request, user)
            request.session['cittadino_email'] = user.email
            # Reindirizza all'area personale
            return redirect('area_personale')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def area_riservata_cittadino(request):
    # Controlla che l'utente è ancora in sessione
    if 'cittadino_email' not in request.session:
        # Se la chiave non è presente, significa che l'utente non è autenticato
        return redirect('login')

    # Verifica che l'utente sia un cittadino
    if request.user.ruolo != 'Cittadino':
        return redirect('home')

    prenotazioni = Prenotazione.objects.filter(utente=request.user).select_related('evento')
    recensioni = Recensione.objects.filter(utente=request.user).select_related('evento')

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

def logout_cittadino(request):
    request.session.flush()

    # Disconnetti l'utente
    logout(request)
    return redirect('home')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = autenticazione_cittadino(username, password)

            if user is None:
                try:
                    # Cerca l'utente con username e ruolo Organizzatore o Amministratore
                    user = Utente.objects.get(username=username)
                    # Verifica la password usando MD5
                    password_md5 = hashlib.md5(password.encode()).hexdigest()
                    if password_md5 != user.password:
                        user = None
                except Utente.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                if user.ruolo == 'Cittadino':
                    request.session['cittadino_email'] = user.email
                    return redirect('area_personale')
                elif user.ruolo == 'Organizzatore':
                    request.session['organizzatore_email'] = user.email
                    return redirect('area_personale')
                elif user.ruolo == 'Amministratore':
                    request.session['amministratore_email'] = user.email
                    return redirect('area_personale')

            form = AuthenticationForm()
            form.errors['__all__'] = form.error_class(['Username o password errati. Riprova.'])
        else:
            form = AuthenticationForm()
            form.errors['__all__'] = form.error_class(['Inserisci username e password.'])
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@role_required('Amministratore')
def ricerca_evento_vulnerabile(request):
    titolo = request.GET.get('titolo', '')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM AgoraCultura_evento WHERE titolo = %s", [titolo])
        risultati = cursor.fetchall()
    return HttpResponse(str(risultati))

@role_required('Organizzatore')
def crea_evento(request):
    if request.method == 'POST':
        form = EventoFormOrganizzatore(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizzatore = request.user
            evento.save()
            # Gestione delle categorie
            categorie = form.cleaned_data.get('categorie')
            for categoria in categorie:
                Associazione.objects.create(evento=evento, categoria=categoria)
            return redirect('dettaglio_evento', evento_id=evento.id)
    else:
        form = EventoFormOrganizzatore()

    return render(request, 'gestione_evento.html', {
        'form': form,
        'titolo_pagina': 'Crea Nuovo Evento'
    })

@role_required('Organizzatore')
def modifica_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    categorie_evento = [assoc.categoria for assoc in Associazione.objects.filter(evento=evento)]

    svolgimento = Svolgimento.objects.filter(evento=evento).first()

    if request.method == 'POST':
        form = EventoFormOrganizzatore(request.POST, instance=evento)
        svolgimento_form = SvolgimentoForm(request.POST, instance=svolgimento) if svolgimento else SvolgimentoForm(request.POST)

        if form.is_valid() and svolgimento_form.is_valid():
            evento = form.save()

            # Aggiorna le categorie
            Associazione.objects.filter(evento=evento).delete()
            categorie = form.cleaned_data.get('categorie')
            for categoria in categorie:
                Associazione.objects.create(evento=evento, categoria=categoria)

            # Salva lo svolgimento
            svolgimento_obj = svolgimento_form.save(commit=False)
            svolgimento_obj.evento = evento
            svolgimento_obj.save()

            return redirect('dettaglio_evento', evento_id=evento.id)
    else:
        form = EventoFormOrganizzatore(instance=evento, initial={'categorie': categorie_evento})
        svolgimento_form = SvolgimentoForm(instance=svolgimento) if svolgimento else SvolgimentoForm()

    return render(request, 'gestione_evento.html', {
        'form': form,
        'svolgimento_form': svolgimento_form,
        'evento': evento,
        'titolo_pagina': 'Modifica Evento'
    })

@role_required('Organizzatore')
def elimina_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    if request.method == 'POST':
        evento.delete()
        return redirect('area_personale')

    return render(request, 'conferma_eliminazione.html', {'evento': evento})

@role_required('Amministratore')
def gestione_utenti(request):
    from .models import Utente
    utenti = Utente.objects.all().order_by('ruolo', 'username')

    return render(request, 'gestione_utenti.html', {
        'utenti': utenti,
    })

@role_required('Amministratore')
def supervisione_eventi(request):
    eventi_da_supervisionare = Evento.objects.filter(
        organizzatore__ruolo='Organizzatore',
        supervisionato=False
    ).select_related('organizzatore')

    eventi_supervisionati = Evento.objects.filter(
        supervisionato=True
    ).select_related('organizzatore')

    return render(request, 'supervisione_eventi.html', {
        'eventi_da_supervisionare': eventi_da_supervisionare,
        'eventi_supervisionati': eventi_supervisionati,
    })

@role_required('Amministratore')
def supervisiona_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    if request.method == 'POST':
        evento.supervisionato = True
        evento.save()
        return redirect('supervisione_eventi')

    return render(request, 'conferma_supervisione.html', {
        'evento': evento,
    })

@role_required('Amministratore')
def modifica_evento_admin(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    categorie_evento = [assoc.categoria for assoc in Associazione.objects.filter(evento=evento)]

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            evento = form.save()

            # Aggiorna le categorie
            Associazione.objects.filter(evento=evento).delete()
            categorie = form.cleaned_data.get('categorie')
            for categoria in categorie:
                Associazione.objects.create(evento=evento, categoria=categoria)

            return redirect('supervisione_eventi')
    else:
        form = EventoForm(instance=evento, initial={'categorie': categorie_evento})

    return render(request, 'gestione_evento.html', {
        'form': form,
        'evento': evento,
        'titolo_pagina': 'Modifica Evento (Admin)'
    })

def logout_view(request):
    if 'cittadino_email' in request.session:
        del request.session['cittadino_email']
    if 'organizzatore_email' in request.session:
        del request.session['organizzatore_email']
    if 'amministratore_email' in request.session:
        del request.session['amministratore_email']

    logout(request)
    return redirect('home')


@csrf_exempt
def login_vulnerabile_cittadino(request): 
    if request.method == "POST":
        email = request.POST.get('email') 
        password = request.POST.get('password') 

        query = f"SELECT * FROM AgoraCultura_utente WHERE email = '{email}'"
        with connection.cursor() as cursor: 
            cursor.execute(query)
            row = cursor.fetchone() 
            if row:
                # Crea un oggetto Utente dai risultati della query
                user_id, password_db, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, ruolo = row

                # Assicuriamoci che l'utente sia un cittadino
                if ruolo != 'Cittadino':
                    # Se non è un cittadino, cerchiamo il primo cittadino nel database
                    cursor.execute("SELECT * FROM AgoraCultura_utente WHERE ruolo = 'Cittadino' LIMIT 1")
                    row = cursor.fetchone()
                    if row:
                        user_id, password_db, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, ruolo = row
                    else:
                        return render(request, 'login_vulnerabile_cittadino.html', {'error': 'Nessun cittadino trovato nel database.'})

                user = Utente(
                    id=user_id,
                    username=username,
                    password=password_db,
                    email=email,
                    ruolo=ruolo
                )

                # Effettua il login dell'utente
                login(request, user)

                # Imposta la variabile di sessione per il cittadino
                request.session['cittadino_email'] = user.email

                # Reindirizza all'area personale
                return redirect('area_personale')
            else:
                return render(request, 'login_vulnerabile_cittadino.html', {'error': 'Credenziali non valide.'})
    else:
        return render(request, 'login_vulnerabile_cittadino.html')


# Funzione di login vulnerabile a SQL injection
def login_vulnerabile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Usa la funzione di autenticazione vulnerabile
            user = autenticazione_vulnerabile(username, password)

            if user is not None:
                login(request, user)
                # Imposta la variabile di sessione in base al ruolo
                if user.ruolo == 'Cittadino':
                    request.session['cittadino_email'] = user.email
                elif user.ruolo == 'Organizzatore':
                    request.session['organizzatore_email'] = user.email
                elif user.ruolo == 'Amministratore':
                    request.session['amministratore_email'] = user.email

                return redirect('area_personale')

            # Se l'autenticazione fallisce, crea un form con errori
            form = AuthenticationForm()
            form.errors['__all__'] = form.error_class(['Username o password errati. Riprova.'])
        else:
            # Se username o password mancano, crea un form con errori
            form = AuthenticationForm()
            form.errors['__all__'] = form.error_class(['Inserisci username e password.'])
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
        'vulnerabile': True  # Flag per indicare che si sta usando la versione vulnerabile
    })

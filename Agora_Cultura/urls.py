"""
Configurazione URL per il progetto Agora_Cultura.

La lista `urlpatterns` indirizza gli URL alle viste. Per maggiori informazioni vedere:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Esempi:
Viste funzione
    1. Aggiungi un import:  from my_app import views
    2. Aggiungi un URL a urlpatterns:  path('', views.home, name='home')
Viste basate su classi
    1. Aggiungi un import:  from other_app.views import Home
    2. Aggiungi un URL a urlpatterns:  path('', Home.as_view(), name='home')
Includere un altro URLconf
    1. Importa la funzione include: from django.urls import include, path
    2. Aggiungi un URL a urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AgoraCultura import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login-vulnerabile/', views.login_vulnerabile, name='login_vulnerabile'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registrazione, name='register'),
    path('calendario/', views.calendario_eventi, name='calendario_eventi'),
    path('evento/<int:evento_id>/', views.dettaglio_evento, name='dettaglio_evento'),
    path('recensione/<int:evento_id>/', views.lascia_recensione, name='recensione_evento'),
    path('area_personale/', views.area_personale, name='area_personale'),
    path('ricerca_vulnerabile/', views.ricerca_evento_vulnerabile, name='ricerca_vulnerabile'),

    # Funzionalità specifiche per cittadini
    path('login-cittadino/', views.login_cittadino, name='login_cittadino'),
    path('area-riservata-cittadino/', views.area_riservata_cittadino, name='area_riservata_cittadino'),
    path('logout-cittadino/', views.logout_cittadino, name='logout_cittadino'),
    path('login-vulnerabile-cittadino/', views.login_vulnerabile_cittadino, name='login_vulnerabile_cittadino'),

    # Gestione eventi per organizzatori
    path('evento/crea/', views.crea_evento, name='crea_evento'),
    path('evento/<int:evento_id>/modifica/', views.modifica_evento, name='modifica_evento'),
    path('evento/<int:evento_id>/elimina/', views.elimina_evento, name='elimina_evento'),

    # Gestione utenti per amministratori
    path('gestione-utenti/', views.gestione_utenti, name='gestione_utenti'),

    # Supervisione eventi per amministratori
    path('supervisione-eventi/', views.supervisione_eventi, name='supervisione_eventi'),
    path('supervisiona-evento/<int:evento_id>/', views.supervisiona_evento, name='supervisiona_evento'),
    path('evento/<int:evento_id>/modifica-admin/', views.modifica_evento_admin, name='modifica_evento_admin'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

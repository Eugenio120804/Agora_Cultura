"""
URL configuration for Agora_Cultura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AgoraCultura import views
from django.contrib.auth import views as auth_views  # ✅ IMPORT NECESSARIO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.registrazione, name='register'),
    path('calendario/', views.home, name='calendario_eventi'),  # se usi `home` come calendario
    path('evento/<int:evento_id>/', views.dettaglio_evento, name='dettaglio_evento'),
    path('recensione/<int:evento_id>/', views.lascia_recensione, name='recensione_evento'),
    path('area_personale/', views.area_personale, name='area_personale'),
]

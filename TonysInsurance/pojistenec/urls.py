from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('uvitani', views.uvitani_view, name='uvitani'),
    path('registrace', views.registrace_view, name='registrace'),
    path('customerlogin', LoginView.as_view(template_name='pojisteni/adminlogin.html'), name='customerlogin'),
    path('pojistenec-profil', views.pojistenec_profil_view, name='pojistenec-profil'),
    path('aktualizace-udaju/<int:pk>', views.aktualizace_udaju_view, name='aktualizace-udaju'),

    path('aktualizace-udaju', views.aktualizace_udaju_view, name='aktualizace-udaju'),

    path('zadost', views.zadost_view, name='zadost'),
    path('zazadat/<int:pk>', views.zazadat_view, name='zazadat'),
    path('archiv', views.archiv_view, name='archiv'),

    path('poslat-dotaz', views.poslat_dotaz_view, name='poslat-dotaz'),
    path('archiv-dotazu', views.archiv_dotazu_view, name='archiv-dotazu'),
]

"""TonysInsurance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from pojisteni import views
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('pojistenec/', include('pojistenec.urls')),
    path('', views.home_view, name=''),
    path('logout', LogoutView.as_view(template_name='pojisteni/logout.html'), name='logout'),
    path('o-nas', views.o_nas_view),
    path('kontakt', views.kontakt_view),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),

    path('adminlogin', LoginView.as_view(template_name='pojisteni/adminlogin.html'), name='adminlogin'),
    path('admin-sprava-pojisteni', views.admin_sprava_pojisteni_view, name='admin-sprava-pojisteni'),

    path('pojistenci', views.pojistenci_view, name='pojistenci'),
    path('pridat-pojistence', views.pridat_pojistence_view, name='pridat-pojistence'),
    path('aktualizace-pojistence/<int:pk>', views.aktualizace_pojistence_view, name='aktualizace-pojistence'),
    path('odstraneni-pojistence/<int:pk>', views.odstraneni_pojistence_view, name='odstraneni-pojistence'),

    path('druhy-pojisteni', views.druhy_pojisteni_view, name='druhy-pojisteni'),
    path('zmenit-nazev-pojisteni/<int:pk>', views.zmenit_nazev_pojisteni_view, name='zmenit-nazev-pojisteni'),
    path('pridat-druh-pojisteni', views.pridat_druh_pojisteni_view, name='pridat-druh-pojisteni'),
    path('smazat-druh-pojisteni/<int:pk>', views.smazat_druh_pojisteni_view, name='smazat-druh-pojisteni'),

    path('pridat-smlouvu', views.pridat_smlouvu_view, name='pridat-smlouvu'),
    path('smlouvy', views.smlouvy_view, name='smlouvy'),
    path('admin-aktualizace-smlouvy', views.admin_aktualizace_smlouvy_view, name='admin-aktualizace-smlouvy'),
    path('aktualizace-smlouvy/<int:pk>', views.aktualizace_smlouvy_view, name='aktualizace-smlouvy'),
    path('zruseni-smlouvy', views.zruseni_smlouvy_view, name='zruseni-smlouvy'),
    path('smazat-smlouvu/<int:pk>', views.smazat_smlouvu_view, name='smazat-smlouvu'),

    path('zobrazeni-navrhu-smluv', views.zobrazeni_navrhu_smluv_view, name='zobrazeni-navrhu-smluv'),
    path('schvalene-navrhy-smluv', views.schvalene_navrhy_smluv_view,
         name='schvalene-navrhy-smluv'),
    path('zamitnute-navrhy-smluv', views.zamitnute_navrhy_smluv_view,
         name='azamitnute-navrhy-smluv'),
    path('cekajici-navrhy-smluv', views.cekajici_navrhy_smluv_view,
         name='cekajici-navrhy-smluv'),
    path('schvalit/<int:pk>', views.schvalit_view, name='schvalit'),
    path('zamitnout/<int:pk>', views.zamitnout_view, name='zamitnout'),

    path('dotazy', views.dotazy_view, name='dotazy'),
    path('odpovedet/<int:pk>', views.odpovedet_view, name='odpovedet'),
    path('smazat-dotaz/<int:pk>', views.smazat_dotaz_view, name='smazat-dotaz'),

]

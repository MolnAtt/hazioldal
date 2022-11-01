from django.contrib import admin
from .models import Dolgozat
from django.contrib.auth.models import User, Group


def teljes_osztaly_hozzarendelese(modeladmin, request, queryset):
    for a_dolgozat in queryset:
        a_dolgozat.tanulok = [t.id for t in sorted(User.objects.filter(groups__name=a_dolgozat.osztaly.name), key=lambda u: u.last_name+u.first_name )]
        a_dolgozat.save()
teljes_osztaly_hozzarendelese.short_description = "Teljes csoport hozzárendelése" 


def list2matrix(elemek, N, M):
    K = len(elemek)
    if K != N*M: 
        raise Exception(f'Baj van, az elemek száma nem egyezik a sorok és oszlopok számával! {K}!={N}*{M}')
    else:
        return [elemek[i:i+M] for i in range(0,K,M)]

def pontmatrix_helyreallitasa(modeladmin, request, queryset):
    for a_dolgozat in queryset:
        a_dolgozat.matrix = list2matrix([ singleton[0] for singleton in a_dolgozat.matrix], len(a_dolgozat.tanulok), len(a_dolgozat.feladatok))
        a_dolgozat.save()
pontmatrix_helyreallitasa.short_description = "Helyreállítás: pontmátrix" 


def osztaly_felvetele(modeladmin, request, queryset):
    for a_dolgozat in queryset:
        a_dolgozat.feladatok = [ user.id for user in sorted(list(User.objects.filter(groups__name=a_dolgozat.osztaly.name)), key=lambda u: u.last_name+u.first_name)]
        a_dolgozat.save()
osztaly_felvetele.short_description = "tanulok := osztaly(abc)" 




class DolgozatAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'email')
    # ordering = ['ev']
    actions = [
            teljes_osztaly_hozzarendelese,
            pontmatrix_helyreallitasa,
        ]
    list_per_page = 200
    
    

admin.site.register(Dolgozat, DolgozatAdmin)


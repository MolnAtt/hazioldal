from django.contrib import admin
from .models import Dolgozat
from django.contrib.auth.models import User, Group


def teljes_osztaly_hozzarendelese(modeladmin, request, queryset:Dolgozat):
    for a_dolgozat in queryset:
        a_dolgozat.tanulok = [t.id for t in sorted(User.objects.filter(groups__name=a_dolgozat.osztaly.name), key=lambda u: u.last_name+u.first_name )]
        a_dolgozat.save()
teljes_osztaly_hozzarendelese.short_description = "Teljes csoport hozzárendelése" 


class DolgozatAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'email')
    # ordering = ['ev']
    actions = [
            teljes_osztaly_hozzarendelese,
        ]
    list_per_page = 200

admin.site.register(Dolgozat, DolgozatAdmin)


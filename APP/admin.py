from django.contrib import admin

from .models import Bigyo, Felhasznalo

admin.site.register(Bigyo)
admin.site.register(Felhasznalo)

# a trükkös admin-funkciókról, függvényekről az szlgbp_ma_heroku gitrepoban vannak jó példák.

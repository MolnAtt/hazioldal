from django.contrib import admin
from .models import Git,Tanit, Mentoral, Temakor, Feladat, Tartozik, Kituzes, Hf, Mo, Biralat

##############################
### GIT

def allapot_count_update(modeladmin, request, queryset):
    for hazioldal_user in queryset:
        hazioldal_user.update_counts()
allapot_count_update.short_description = "Állapotszámok frissítése"

class GitAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'email')
    # ordering = ['ev']
    actions = [
            allapot_count_update,
        ]
    list_per_page = 200

admin.site.register(Git, GitAdmin)


##############################
### HF

def allapot_count_update(modeladmin, request, queryset):
    for hf in queryset:
        hf.update_allapot()
allapot_count_update.short_description = "Állapot frissítése"

class HfAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'email')
    # ordering = ['ev']
    actions = [
            allapot_count_update,
        ]
    list_per_page = 1000

admin.site.register(Hf, HfAdmin)

##############################
### 

admin.site.register(Tanit)
admin.site.register(Mentoral)
admin.site.register(Temakor)
admin.site.register(Feladat)
admin.site.register(Tartozik)
admin.site.register(Kituzes)
admin.site.register(Mo)
admin.site.register(Biralat)

# a trükkös admin-funkciókról, függvényekről az szlgbp_ma_heroku gitrepoban vannak jó példák.


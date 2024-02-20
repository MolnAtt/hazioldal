from django.urls import path
from .views import index, hazik, hf, regisztracio, kituz, adminisztracio, fiok, ellenorzes_csoportvalasztas_tanarnak, ellenorzes_tanarnak, ellenorzes_mentoraltnak, ellenorzes_mentornak,ellenorzes_csoportvalasztas_mentornak, haladekopciok, haladek_egyeb
from APP.views_api import create_git_for_all, update_git
from APP.views_api import read_hf, update_hf, update_all_hf
from APP.views_api import create_mo
from APP.views_api import create_biralat, delete_biralat
from APP.views_api import create_users, update_activity
from APP.views_api import create_mentoral_tsv, create_mentoral_tanar, read_mentoral
from APP.views_api import read_tema_feladatai
from APP.views_api import create_kituzes
from APP.views_api import amnesztia
from APP.views_api import egyesek_mennyilenne, egyesek_rogzitese

urlpatterns = [
    path('', index),
    path('hazioldal/attekintes/mo/uj/', index),
    path('hf/<int:hfid>/', hf),
    path('hf/<int:hfid>/haladek/', haladekopciok),
    path('hf/<int:hfid>/haladek/mentoralas/', haladek_egyeb),
    path('hf/<int:hfid>/haladek/<str:tipus>/', haladek_egyeb),
    path('tanar/regisztracio/', regisztracio, name='tanar_regisztracio'),
    path('tanar/kituz/', kituz, name='tanar_kituz'),
    path('mentoralt/ellenorzes/', ellenorzes_mentoraltnak, name='mentoralt_ellenorzes'),
    path('mentor/ellenorzes/', ellenorzes_csoportvalasztas_mentornak, name='mentor_csoportvalasztas'),
    path('mentor/ellenorzes/<str:csoport>/', ellenorzes_mentornak, name='mentor_ellenorzes'),
    path('tanar/ellenorzes/', ellenorzes_csoportvalasztas_tanarnak, name='tanar_csoportvalasztas'),
    path('tanar/ellenorzes/<str:csoport>/', ellenorzes_tanarnak, name='tanar_ellenorzes'),
    path('fiok/', fiok),
    path('adminisztracio/', adminisztracio),
]


# API

urlpatterns += [
    path('api/get/feladat/read/tema/<int:temaid>/', read_tema_feladatai),
    path('api/get/hf/read/<int:hfid>/', read_hf),
    path('api/post/hf/update/<int:hfid>/', update_hf),
    path('api/post/hf/update_all/', update_all_hf),
    path('api/post/mo/create/hf/<int:hfid>/', create_mo),
    path('api/post/biralat/create/hf/<int:hfid>/', create_biralat),
    path('api/delete/biralat/<int:biralatid>/', delete_biralat),
    path('api/post/user/create/', create_users),
    path('api/post/mentoral/create/tsv/', create_mentoral_tsv),
    path('api/post/mentoral/create/tanar/', create_mentoral_tanar),
    path('api/get/mentoral/<str:mit>/read/', read_mentoral),
    path('api/post/kituzes/create/', create_kituzes),
    path('api/post/user/update/activity/', update_activity),
    path('api/post/amnesztia/', amnesztia),
    path('api/post/git/create/all/', create_git_for_all),
    path('api/post/git/update/', update_git),
    path('api/get/egyes/<str:csoportnev>/mennyilenne/', egyesek_mennyilenne ),
    path('api/post/egyes/<str:csoportnev>/create/', egyesek_rogzitese ),
]

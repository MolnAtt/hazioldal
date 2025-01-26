from django.urls import path
from .views import *
from APP.views_api import *

urlpatterns = [
    path('', index),
    path('hazioldal/attekintes/mo/uj/', index),
    path('hf/<int:hfid>/', ujhf),
    path('hf/<int:hfid>/haladek/', haladekopciok),
    path('hf/<int:hfid>/haladek/mentoralas/', haladek_mentoralas),
    path('hf/<int:hfid>/haladek/mentoralas/post/', haladek_mentoralas_post),
    path('haladek/', haladekok, name="haladekok"),
    path('haladek/<int:haladekid>/', haladek),
    path('haladek/<int:haladekid>/elfogad/', haladek_elfogad),
    path('haladek/<int:haladekid>/fuggeszt/', haladek_fuggeszt),
    path('haladek/<int:haladekid>/elutasit/', haladek_elutasit),
    path('haladek/<int:haladekid>/torol/', haladek_torol),
    path('hf/<int:hfid>/haladek/<str:tipus>/', haladek_egyeb),
    path('hf/<int:hfid>/haladek/<str:tipus>/post/', haladek_egyeb_post),
    path('tanar/regisztracio/', regisztracio, name='tanar_regisztracio'),
    path('tanar/kituz/', kituz, name='tanar_kituz'),
    path('mentoralt/ellenorzes/', hazinezet, name='mentoralt_ellenorzes'),
    path('mentor/ellenorzes/', ellenorzes_csoportvalasztas_mentornak, name='mentor_csoportvalasztas'),
    path('mentor/ellenorzes/<str:csoport>/', uj_mentor_ellenorzes, name='mentor_ellenorzes'),
    path('tanar/ellenorzes/', ellenorzes_csoportvalasztas_tanarnak, name='tanar_csoportvalasztas'),
    path('tanar/ellenorzes/<str:csoport>/', uj_mentor_ellenorzes, name='tanar_ellenorzes'),
    path('fiok/', fiok),
    path('kampany/<int:kampanyid>/', kampany),
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
    path('api/post/resetnullas/', resetnullas, name='resetnullas'),
    path('api/post/kozpercek/update/', change_kozpercek, name='change_kozpercek'),
    path('api/post/feladat/create/', create_feladat, name='create_feladat'),
    path('api/post/temakor/create/', create_temakor, name='create_temakor'),
    path('api/post/user/update/activity/', update_activity),
    path('api/post/amnesztia/', amnesztia),
    path('api/post/git/create/all/', create_git_for_all),
    path('api/post/git/update/', update_git),
    path('api/get/egyes/<str:csoportnev>/mennyilenne/', egyesek_mennyilenne ),
    path('api/post/egyes/<str:csoportnev>/create/', egyesek_rogzitese ),
    path('api/get/haladek/feladatlekeres/<int:mentoralt_id>/', feladatok_frissitese),
    path('api/get/haladek/feladatlekeres/<int:mentoralt_id>/<int:feladat_id>/', biralatok_frissitese),
]

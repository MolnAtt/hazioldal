from django.contrib import admin
from django.urls import path, include
from APP.views import index, hazik, hf, regisztracio, kituz, adminisztracio, fiok
from APP.views_api import create_git_for_all, update_git
from APP.views_api import read_hf, update_hf
from APP.views_api import create_mo
from APP.views_api import create_biralat, delete_biralat
from APP.views_api import create_users, update_activity
from APP.views_api import create_mentoral_tsv, create_mentoral_tanar, read_mentoral
from APP.views_api import read_tema_feladatai
from APP.views_api import create_kituzes

# VIEWS

urlpatterns = [
    path('', index),
    path('attekintes/<str:hfmo>/<str:szuro>/', hazik),
    path('hf/<int:hfid>/', hf),
    path('tanar/regisztracio/', regisztracio),
    path('tanar/kituz/', kituz),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('fiok/', fiok),
    path('adminisztracio/', adminisztracio),
]

# API

urlpatterns += [
   	path('api/get/feladat/read/tema/<int:temaid>/', read_tema_feladatai),
   	path('api/get/hf/read/<int:hfid>/', read_hf),
   	path('api/post/hf/update/<int:hfid>/', update_hf),
    path('api/post/mo/create/hf/<int:hfid>/', create_mo),
    path('api/post/biralat/create/hf/<int:hfid>/', create_biralat),
    path('api/delete/biralat/<int:biralatid>/', delete_biralat),
    path('api/post/user/create/', create_users),
    path('api/post/mentoral/create/tsv/', create_mentoral_tsv),
    path('api/post/mentoral/create/tanar/', create_mentoral_tanar),
    path('api/get/mentoral/<str:mit>/read/', read_mentoral),
    path('api/post/kituzes/create/', create_kituzes),
    path('api/post/user/update/activity/', update_activity),
    path('api/post/git/create/all/', create_git_for_all),
    path('api/post/git/update/', update_git),
]
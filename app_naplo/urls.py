
from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import render, redirect
from app_naplo.views import felhasznalok_regisztracioja, dolgozat, csoportvalaszto, dolgozatvalaszto, index, dolgozatmatrixeditor, dolgozat_download, ellenorzo, tanulo_redirect, tanulo_dolgozata, ujdolgozat, ellenorzo_csoportvalaszto, index_ev
from app_naplo.api import create_users, write_pont, write_suly, write_ponthatar, create_dolgozat, read_dolgozat


# VIEWS

urlpatterns = [
    path('', index),
    path('<int:ev>/', index_ev),
    path('<int:ev>/csoport/regisztracio/', felhasznalok_regisztracioja),
    path('<int:ev>/csoport/', csoportvalaszto),
    path('<int:ev>/csoport/<str:group_name>/ujdolgozat/', ujdolgozat),
    path('<int:ev>/csoport/<str:group_name>/', dolgozatvalaszto),
    path('<int:ev>/csoport/<str:group_name>/<str:dolgozat_slug>/', dolgozat),
    path('<int:ev>/csoport/<str:group_name>/<str:dolgozat_slug>/download/', dolgozat_download),
    path('<int:ev>/dolgozat/<str:group_name>/<str:dolgozat_slug>/', dolgozatmatrixeditor),
    path('<int:ev>/tanulo/', tanulo_redirect),
    path('<int:ev>/tanulo/<int:tanuloid>/', ellenorzo_csoportvalaszto),
    path('<int:ev>/tanulo/<int:tanuloid>/csoport/<str:group_name>/', ellenorzo),
    path('<int:ev>/tanulo/<int:tanuloid>/dolgozat/<str:dolgozat_slug>/', tanulo_dolgozata),
]

# API

urlpatterns += [
    path('api/post/user/create/', create_users),
    path('api/post/pont/write/<str:group_name>/<str:dolgozat_slug>/', write_pont),
    path('api/post/suly/write/<str:group_name>/<str:dolgozat_slug>/', write_suly),
    path('api/post/ponthatar/write/<str:group_name>/<str:dolgozat_slug>/', write_ponthatar),
    path('api/post/dolgozat/create/', create_dolgozat),
    path('api/post/dolgozat/read/<str:group_name>/<str:dolgozat_slug>/<int:tanulo_id>/', read_dolgozat),
]

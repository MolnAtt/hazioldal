
from django.contrib import admin
from django.urls import path, include
from app_naplo.views import felhasznalok_regisztracioja, dolgozat, csoportvalaszto, dolgozatvalaszto, index, dolgozatmatrixeditor, dolgozat_download, tanuloi_dolgozatvalaszto, tanulo_redirect, tanuloi_kimutatas, ujdolgozat
from app_naplo.api import create_users, write_pont, write_ponthatar, create_dolgozat, read_dolgozat


# VIEWS

urlpatterns = [
    path('', index),
    path('regisztracio/', felhasznalok_regisztracioja),
    path('csoport/', csoportvalaszto),
    path('csoport/<str:group_name>/', dolgozatvalaszto),
    path('csoport/<str:group_name>/uj_dolgozat/', ujdolgozat),
    path('csoport/<str:group_name>/<str:dolgozat_slug>/', dolgozat),
    path('csoport/<str:group_name>/<str:dolgozat_slug>/download/', dolgozat_download),
    path('dolgozat/<str:group_name>/<str:dolgozat_slug>/', dolgozatmatrixeditor),
    path('tanulo/', tanulo_redirect),
    path('tanulo/<int:tanuloid>/', tanuloi_dolgozatvalaszto),
    path('tanulo/<int:tanuloid>/<str:dolgozat_slug>/', tanuloi_kimutatas),
]

# API

urlpatterns += [
    path('api/post/user/create/', create_users),
    path('api/post/pont/write/<str:group_name>/<str:dolgozat_slug>/', write_pont),
    path('api/post/ponthatar/write/<str:group_name>/<str:dolgozat_slug>/', write_ponthatar),
    path('api/post/dolgozat/create/', create_dolgozat),
    path('api/post/dolgozat/read/<str:group_name>/<str:dolgozat_slug>/', read_dolgozat),
]

from django.contrib import admin
from django.urls import path, include
from app_naplo.views import felhasznalok_regisztracioja, dolgozat, csoportvalaszto, dolgozatvalaszto, index, dolgozatmatrixeditor, dolgozat_download
from app_naplo.api import create_users, write_pont


# VIEWS

urlpatterns = [
    path('', index),
    path('regisztracio/', felhasznalok_regisztracioja),
    path('csoport/', csoportvalaszto),
    path('csoport/<str:group_name>/', dolgozatvalaszto),
    path('csoport/<str:group_name>/<str:dolgozat_slug>/', dolgozat),
    path('csoport/<str:group_name>/<str:dolgozat_slug>/download/', dolgozat_download),
    path('dolgozat/<str:group_name>/<str:dolgozat_slug>/', dolgozatmatrixeditor),
]

# API

urlpatterns += [
    path('api/post/user/create/', create_users),
    path('api/post/pont/write/<str:group_name>/<str:dolgozat_slug>/', write_pont),
]

from django.contrib import admin
from django.urls import path, include
from app_naplo.views import felhasznalok_regisztracioja, dolgozat, csoportvalaszto, dolgozatvalaszto, index, dolgozatmatrixeditor
from app_naplo.api import create_users, write_pont


# VIEWS

urlpatterns = [
    path('', index),
    path('regisztracio/', felhasznalok_regisztracioja),
    path('csoport/', csoportvalaszto),
    path('csoport/<str:group_name>/', dolgozatvalaszto),
    path('csoport/<str:group_name>/<str:dolgozat_slug>/', dolgozat),
    path('dolgozat/<str:group_name>/<str:dolgozat_slug>/', dolgozatmatrixeditor),
]

# API

urlpatterns += [
    path('api/post/user/create/', create_users),
    path('api/post/pont/write/', write_pont),
]
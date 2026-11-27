from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from APP.views import kezdolap


urlpatterns = [
    path('', kezdolap, name='kezdolap'),
    path('hazioldal/', include('APP.urls')),
    path('naplo/', include('app_naplo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls, {'extra_context': {'subtitle': 'alcim'}}),
]


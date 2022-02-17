from django.contrib import admin
from django.urls import path, include
from APP.views import index, hazik, hf, regisztracio
from APP.views_api import hf_read, update_hf
from APP.views_api import create_mo
from APP.views_api import create_biralat, delete_biralat
from APP.views_api import create_users
from APP.views_api import create_mentoral

# VIEWS

urlpatterns = [
    path('', index),
    path('attekintes/<str:hfmo>/<str:szuro>/', hazik),
    path('hf/<int:hfid>/', hf),
    path('tanar/regisztracio/', regisztracio),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

# API

urlpatterns += [
   	path('api/get/hf/read/<int:hfid>/', hf_read),
   	path('api/post/hf/update/<int:hfid>/', update_hf),
    path('api/post/mo/create/hf/<int:hfid>/', create_mo),
    path('api/post/biralat/create/hf/<int:hfid>/', create_biralat),
    path('api/delete/biralat/<int:biralatid>/', delete_biralat),
    path('api/post/user/create/', create_users),
    path('api/post/mentoral/create/', create_mentoral),
]
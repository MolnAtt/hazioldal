from django.contrib import admin
from django.urls import path, include
from APP.views import index, hazik, repo, repo_create, mentoralas
from APP.views_api import create_repo, read_repo, update_repo, delete_repo
from APP.views_api import create_mo
from APP.views_api import create_biralat, delete_biralat

urlpatterns = [
    path('', index),
    path('attekintes/<str:hfmo>/<str:szuro>/', hazik),
    path('hf/<str:szuro>/', hazik),
    path('repo/<int:repoid>/', repo),
    path('hf/<int:hfid>/repo/create/', repo_create),
    path('mentoralas/<str:szuro>/', mentoralas),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

   	path('api/post/repo/create/<int:hfid>/', create_repo),
   	path('api/get/repo/get/<int:repoid>/', read_repo),
   	path('api/post/repo/update/<int:repoid>/', update_repo),
   	path('api/delete/repo/delete/<int:repoid>/', delete_repo),

    path('api/post/mo/create/repo/<int:repoid>/', create_mo),
    
    path('api/post/biralat/create/repo/<int:repoid>/', create_biralat),
    path('api/delete/biralat/<int:biralatid>/', delete_biralat),
]

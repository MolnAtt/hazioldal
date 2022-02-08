from django.contrib import admin
from django.urls import path, include
from APP.views import index, hazik, repo_check, repo, repo_create, mentoralas, repo_forum
from APP.views_api import create_repo, read_repo, update_repo, delete_repo

urlpatterns = [
    path('', index),
    path('hf/<str:szuro>/', hazik),
    path('hf/<int:hfid>/repo/', repo_check),
    path('repo/<int:repoid>/', repo),
    path('hf/<int:hfid>/repo/create/', repo_create),
    path('repo/<int:repoid>/mo/', repo_forum),
    
    path('mentoralas/<str:szuro>/', mentoralas),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

   	path('api/post/repo/create/<int:hfid>/', create_repo),
   	path('api/get/repo/get/<int:repoid>/', read_repo),
   	path('api/post/repo/update/<int:repoid>/', update_repo),
   	path('api/delete/repo/delete/<int:repoid>/', delete_repo),

]

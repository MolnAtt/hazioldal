from django.contrib import admin
from django.urls import path, include
from APP.views import index, hazik, repo_check, repo_editor, repo_create
from APP.views_api import get_repo, delete_repo, update_repo

urlpatterns = [
    path('', index),
    path('hf/<str:szuro>/', hazik),
    path('hf/<int:hfid>/repo/', repo_check),
    path('hf/<int:hfid>/repo/edit/<int:repoid>/', repo_editor),
    path('hf/<int:hfid>/repo/create/', repo_create),
    path('repo/<int:repoid>/', repo_editor),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

   	path('api/get/repo/get/<int:repoid>/', get_repo),
   	path('api/post/repo/update/<int:repoid>/', update_repo),
   	path('api/delete/repo/delete/<int:repoid>/', delete_repo),

]

from django.contrib import admin
from django.urls import path, include
from APP.views import hazik, api_get_var, api_get_all, api_get_one, api_create, api_update, api_delete

urlpatterns = [
    path('hf/<str:szuro>/', hazik),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

   	path('api/get/variable/', api_get_var),
   	path('api/get/model-object/all/', api_get_all),
   	path('api/get/model-object/this/<str:pk>/', api_get_one),
   	path('api/post/create/', api_create),
   	path('api/post/update/<str:pk>/', api_update),
   	path('api/delete/<str:pk>/', api_delete),

	# path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
	# path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
]

from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('account.urls')),
    path('' , include('tasks.urls')),
    path('' , include('projects.urls')),
    path('api-auth/', include('rest_framework.urls'))

]

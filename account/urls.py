from django.contrib import admin
from django.urls import path

from rest_framework import routers
from rest_framework.authtoken import views

from . import views as vw


app_name = "users"
router = routers.SimpleRouter()

router.register(r'user',vw.UserViewSet,basename = "users")
router.register(r'team',vw.TeamViewSet,basename = "teams")

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token)
]

urlpatterns += router.urls

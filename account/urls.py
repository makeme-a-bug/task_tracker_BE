from django.contrib import admin
from django.urls import path

from rest_framework import routers
from rest_framework.authtoken import views

from . import views as vw


app_name = "users"
router = routers.SimpleRouter()

router.register(r'user',vw.UserViewSet,basename = "users")

urlpatterns = [
    path('api-token-auth/', vw.CustomAuthToken.as_view())
]

urlpatterns += router.urls

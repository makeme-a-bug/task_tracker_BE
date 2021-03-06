from django.contrib import admin
from django.urls import path

from rest_framework import routers

from . import views as vw


app_name = "projects"
router = routers.SimpleRouter()

router.register(r'project',vw.ProjectViewSet,basename = "projects")
router.register(r'(?P<project>[^/.]+)/role',vw.RoleViewSet,basename = "roles")
router.register(r'(?P<project>[^/.]+)/status',vw.StatusViewSet,basename = "status")
router.register(r'permissions',vw.PermissionViewSet,basename = "permissions")
 
urlpatterns = router.urls

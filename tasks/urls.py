from django.contrib import admin
from django.urls import path
from . import views as vw
from rest_framework import routers

app_name = "tasks"

router = routers.SimpleRouter()
router.register(r'(?P<project>[^/.]+)/task', vw.TasksViewSet , basename="tasks")
router.register(r'(?P<task>[^/.]+)/issue', vw.IssueViewSet , basename="tasks")
router.register(r'(?P<task>[^/.]+)/taskComment', vw.TaskCommentViewSet , basename="tasks")
router.register(r'(?P<issue>[^/.]+)/issueComment', vw.IssueCommentViewSet , basename="tasks")



urlpatterns = router.urls

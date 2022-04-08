from msilib.schema import ProgId
from django.contrib import admin

from .models import Project,Role,Permission,Status

admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Status)
# Register your models here.

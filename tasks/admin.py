from django.contrib import admin

from .models import Task , Comment , Issue , TaskComment , IssueComment
# Register your models here.

admin.site.register(Task)
admin.site.register(Issue)
admin.site.register(TaskComment)
admin.site.register(IssueComment)

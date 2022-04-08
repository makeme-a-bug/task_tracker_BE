from rest_framework import permissions
from account.models import User

class TaskPermission(permissions.BasePermission):
    message = 'This operation is not allowed under your role'

    def has_permission(self, request, view):
        user = User.objects.get(email="admin@gmail.com")
        project = request.parser_context['kwargs'].get('project',None)
        roles = user.role_set.filter(project__id = project)
        codeName = ""
        if view.action in ['list','retrieve','individualTasks']:
            codeName = 'can_retrieve'
        elif view.action in ['update','partial_update']:
            codeName = 'can_update'
        elif view.action in ['create']:
            codeName = 'can_create'
        elif view.action in ['destroy']:
            codeName = 'can_delete'
        for r in roles:
            if r.permissions.filter(codeName=codeName,model="task").exists():
                return True
        return False
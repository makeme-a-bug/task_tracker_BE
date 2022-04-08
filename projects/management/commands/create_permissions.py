from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import Permission

class Command(BaseCommand):
    help = 'creats permissions'

    def handle(self, *args, **kwargs):
        models = ["task","issue","taskcomment","issuecomment","project","role","permission","status"]
        perm_typs = ['can_create','can_retrieve','can_delete','can_update']
        for model in models:
            for perm_typ in perm_typs:
                description = perm_typ.replace("_"," ")
                if not Permission.objects.filter(codeName=perm_typ,model=model).exists():
                    Permission.objects.get_or_create(codeName=perm_typ,model=model,description=f"{description} {model}")
        
        user_perm_types = ['can_invite','can_change_role','can_remove_role','can_remove']
        model = "user"
        for perm_typ in user_perm_types:
                description = perm_typ.replace("_"," ")
                if not Permission.objects.filter(codeName=perm_typ,model=model).exists():
                    Permission.objects.get_or_create(codeName=perm_typ,model=model,description=f"{description} {model}")
        
        self.stdout.write("Permissions created")

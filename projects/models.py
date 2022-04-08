from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User
import nanoid

def getID():
    return str(nanoid.generate(size=15))

def getCurrentUnixTime():
    return timezone.now().timestamp()

class Project(models.Model):
    id = models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID, editable=False) 
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.FloatField(default=getCurrentUnixTime, editable=False)
    members = models.ManyToManyField(User , related_name="project_members", blank=True)

    class Meta:
        unique_together = ('title', 'user')

class Status(models.Model):
    id = models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID, editable=False)
    project = models.ForeignKey(Project,on_delete=models.CASCADE , related_name="status_project")
    name = models.CharField(max_length=50)
    created_on = models.FloatField(default = getCurrentUnixTime , editable=False)
    color = models.CharField(max_length=16)

    class Meta:
        unique_together = ('project', 'name')


class Permission(models.Model):
    id = models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID, editable=False)
    codeName = models.TextField()
    description = models.TextField()
    model = models.TextField()

    def __str__(self):
        return self.codeName+" | "+self.model

class Role(models.Model):
    id = models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    color = models.CharField(max_length=10,default="#dddddd")
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)
    deletable = models.BooleanField(default=True , editable=False)
    permissions = models.ManyToManyField(Permission, blank=True)
    class Meta:
        unique_together = ('project', 'name')

    def __str__(self):
        return self.name+" "+self.project.title


@receiver(post_save, sender=Project)
def create_status(sender, instance, created, **kwargs):

    STATUS = [{"name":"Panning","color":"#126caa"},{"name":"Implementing","color":"#C446FF"},{"name":"Completed","color":"#44AF69"}]
    if created:
        for s in STATUS:
            Status.objects.create(name = s['name'] , color=s['color'] , project = instance)
        R = Role.objects.create(name="Creator",description="Creator of the project",color="#44AF69",project=instance,deletable=False)
        R.permissions.add(*list(Permission.objects.all()))
        R.users.add(instance.user)
        instance.members.add(instance.user)
        instance.save()


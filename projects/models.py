from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User , Team
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
    teams = models.ManyToManyField(Team, related_name="account_team" , blank=True )
    members = models.ManyToManyField(User , related_name="project_members", blank=True)

    # class Meta:
    #     unique_together = ('title', 'user')

class Status(models.Model):
    id = models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID, editable=False)
    project = models.ForeignKey(Project,on_delete=models.CASCADE , related_name="status_project")
    name = models.CharField(max_length=50)
    created_on = models.FloatField(default = getCurrentUnixTime , editable=False)
    color = models.CharField(max_length=16)

    class Meta:
        unique_together = ('project', 'name')
        
@receiver(post_save, sender=Project)
def create_status(sender, instance, created, **kwargs):

    STATUS = [{"name":"Panning","color":"#126caa"},{"name":"Implementing","color":"#C446FF"},{"name":"Completed","color":"#44AF69"}]
    if created:
        for s in STATUS:
            Status.objects.create(name = s['name'] , color=s['color'] , project = instance)
    

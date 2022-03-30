from turtle import mode
from django.db import models
from django.utils import timezone
from projects.models import Project , Status
from account.models import User

import nanoid

def getID():
    return str(nanoid.generate(size=10))

def getCurrentUnixTime():
    return timezone.now().timestamp()

STATUS = (("IP","In Progress") , ("DO","Done") , ("SB" , "Stand By") , ("OH","On Hold"))

ISSUE_STATUS = (("UR","Under Reveiw"),("RS","Resolved"),("OP","Open"))

TASK_TYPE = (("mn","Main task"),("sub","Sub task"))

PRIORITY = (("nr","Normal"),("md","Medium"),("hg","High"))

#add sub status like active,onhold ,done
class Task(models.Model):
    id = models.CharField(max_length=15 , unique=True , primary_key=True , editable=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    assigne = models.ManyToManyField(User, related_name="assigne",blank=True)
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=3 , default="nl")
    description = models.TextField()
    created_on = models.FloatField(default = getCurrentUnixTime , editable=False)
    starts_on = models.FloatField(blank=True, null=True)
    ends_on = models.FloatField(blank=True, null=True)
    status = models.ForeignKey(Status , on_delete=models.SET_NULL , null = True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    type = models.CharField(max_length=3 , choices = TASK_TYPE , default = "mn")

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.project.title[:2]+self.project.title[-2:]+"_"+ str(len(Task.objects.all())+1)
            print("ok")
        super().save(*args, **kwargs)

class Issue (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    id = models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.FloatField(default = getCurrentUnixTime)
    status = models.CharField(choices = ISSUE_STATUS , default="" , max_length=3)
    task = models.ForeignKey(Task , on_delete=models.CASCADE)


class Comment (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    id= models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID, editable=False)
    comment = models.TextField()
    created_on = models.FloatField(default = getCurrentUnixTime)
    class Meta:
        abstract = True

class TaskComment(Comment):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class IssueComment(Comment):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)



# Create your models here.

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager


import nanoid

def getID():
    return str(nanoid.generate(size=15))
    
def getCurrentUnixTime():
    return timezone.now().timestamp()

account_role = (("super","super_user"),("admin","Account_admin"),("member","member"))
account_type = (("basic","basic"),)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    
    id = models.CharField(max_length=15 , unique=True , primary_key=True ,default=getID)
    username = None
    email = models.EmailField('email address', unique=True)
    role = models.CharField(max_length=25 , choices =account_role , default="admin")
    type = models.CharField(max_length=25 , choices =account_type , default="basic")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()






class Team(models.Model):
    name = models.CharField(max_length=100, unique=True , primary_key=True)
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    head = models.ForeignKey(User , on_delete= models.DO_NOTHING, related_name='head')
    members = models.ManyToManyField(User, related_name='members')
    created_on = models.FloatField(default=getCurrentUnixTime)
    description = models.TextField()

    class Meta:
        unique_together = ('user', 'name')


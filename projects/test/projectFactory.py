
from faker import Faker as FakerClass
from typing import Any, Sequence
from factory import django, Faker, post_generation,PostGenerationMethodCall


from projects.models import Project,Role,Status
from account.models import User
from account.test.userFactory import UserFactory as UF


class ProjectFactory(django.DjangoModelFactory):
    
    class Meta:
        model = Project

    title = Faker('name')
    description = Faker('address')

class RoleFactory(django.DjangoModelFactory):
        
    class Meta:
        model = Role
    
    name = Faker('name')
    description = Faker('address')


class StatusFactory(django.DjangoModelFactory):
        
    class Meta:
        model = Role
    
    name = FakerClass().name()
    color = Faker('color')


def create_test_data():
    users = UF.create_batch(5)
    projects = []
    roles = []
    for u in users:
        projects.extend(ProjectFactory.create_batch(5,user = u ))
    for p in projects:
        roles.extend(RoleFactory.create_batch(2,project = p ))
    
    return projects,roles,users
    
    
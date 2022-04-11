from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from account.test.userFactory import UserFactory,AdminUserFactory
from account.models import User
from projects.models import Project,Status,Role
from projects.test.projectFactory import create_test_data

from faker import Faker

class ProjectViewSetTestCase(APITestCase):
    #need test for invalid data
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.projects,cls.roles,cls.users = create_test_data()
        cls.admin_user = AdminUserFactory.create()
        cls.client = APIClient()
        cls.list_url = reverse('projects:projects-list')
        cls.get_url = 'projects:projects-detail'
        cls.get_members_url = 'projects:projects-members'
        cls.faker_obj = Faker()

    def test_project_list(self):
        user = self.users[0]
        token,created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Project.objects.filter(user = user)))

    def test_project_get(self):
        user = self.users[0]
        project = Project.objects.filter(user = user)[0]
        token,created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse(self.get_url, kwargs={'pk': project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], project.id)

    def test_project_update(self):
        user = self.users[0]
        project = Project.objects.filter(user = user)[0]
        token,created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        update_dict = {
            'title': self.faker_obj.name(),
            'description': self.faker_obj.address(),
        }

        response = self.client.patch(reverse(self.get_url, kwargs={'pk': project.id}),update_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], update_dict['title'])
        self.assertEqual(response.data['description'], update_dict['description'])
    
    def test_project_update_add_members(self):
        user = self.users[0]
        project = Project.objects.filter(user = user)[0]
        token,created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        update_dict = {
            'members': [ u.id for u in self.users],
        }

        response = self.client.patch(reverse(self.get_url, kwargs={'pk': project.id}),update_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['members']), len(self.users))

    def test_project_destroy(self):
        user = self.users[0]
        project = Project.objects.create(user = user,title = "lamo",description = "lamo")
        count = Project.objects.filter(user = user).count()
        token,created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(reverse(self.get_url, kwargs={'pk': project.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.filter(user = user).count(),count -1)
        
    def test_project_members(self):
        user = self.users[0]
        project = Project.objects.filter(user = user)[0]
        token,created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse(self.get_members_url, kwargs={'pk': project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(project.members.all()))
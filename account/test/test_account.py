from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from account.test.userFactory import UserFactory,AdminUserFactory
from account.models import User

from faker import Faker

#add test for get user detial , put user, delete user , patch user

class UserViewSetTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = UserFactory.build()
        cls.user_saved = UserFactory.create()
        cls.admin_user = AdminUserFactory.create()
        cls.client = APIClient()
        cls.signup_url = reverse('users:users-signup')
        cls.login_url = reverse('users:users-login')
        cls.list_url = reverse('users:users-list')
        cls.get_url = 'users:users-detail'
        cls.faker_obj = Faker()


    def test_list(self):
        token,created = Token.objects.get_or_create(user=User.objects.get(email=self.admin_user.email))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

    def test_list_with_no_admin_authorization(self):
        token,created = Token.objects.get_or_create(user=User.objects.get(email=self.user_saved.email))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(len(response.data), 2)

    def test_if_data_is_correct_then_login(self):

        login_dict = {
            'email': self.user_saved.email,
            'password': self.user_saved.password,
        }

        response = self.client.post(self.login_url,  login_dict)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_obj = User.objects.get(email=self.user_saved.email)
        token= Token.objects.get(user=user_obj)
        self.assertEqual(response.data['user']['email'], self.user_saved.email)
        self.assertEqual(response.data['token'], str(token))


    
    def test_if_email_is_invalid_when_loging_in(self):

        login_dict = {
            'email': self.faker_obj.name(),
            'password': self.user_saved.password,
        }

        response = self.client.post(self.login_url,  login_dict)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "email or password is incorrect")


    def test_if_data_is_correct_then_signup(self):

        signup_dict = {
            'email': self.user_object.email,
            'password': 'test_Pass',
        }

        response = self.client.post(self.signup_url, signup_dict)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

        new_user = User.objects.get(email=self.user_object.email)

    def test_if_no_email_and_pass_provided(self):

        signup_dict = {
            'email': '',
            'password': '',
        }

        response = self.client.post(self.signup_url, signup_dict)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['email'][0]),
            'This field may not be blank.',
        )
        self.assertEqual(
            str(response.data['password'][0]),
            'This field may not be blank.',

        )

        username_query = User.objects.filter(email=self.user_saved.email)
        self.assertEqual(username_query.count(), 1)
    
    def test_if_no_email_is_invalid(self):
        # Prepare data with already saved user
        signup_dict = {
            'email': self.faker_obj.name(),
            'password': 'test_pass',
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['email'][0]),
            'Enter a valid email address.',
        )
        # Check database
        # Check that there is only one user with the saved username
        username_query = User.objects.filter(email=self.user_saved.email)
        self.assertEqual(username_query.count(), 1)

    def test_if_no_password_is_provided(self):
        # Prepare data with already saved user
        signup_dict = {
            'email': self.faker_obj.email(),
            'password': '',
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['password'][0]),
            'This field may not be blank.',
        )
        # Check database
        # Check that there is only one user with the saved username
        username_query = User.objects.filter(email=self.user_saved.email)

    def test_if_username_already_exists_dont_signup(self):
        # Prepare data with already saved user
        signup_dict = {
            'email': self.user_saved.email,
            'password': 'test_Pass',
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['email'][0]),
            'user with this email address already exists.',
        )
        # Check database
        # Check that there is only one user with the saved username
        username_query = User.objects.filter(email=self.user_saved.email)
        self.assertEqual(username_query.count(), 1)

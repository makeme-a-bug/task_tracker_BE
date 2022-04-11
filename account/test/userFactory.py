from faker import Faker as FakerClass
from typing import Any, Sequence
from factory import django, Faker, post_generation,PostGenerationMethodCall
from account.models import User



class UserFactory(django.DjangoModelFactory):

    def __init__(self, *args, **kwargs):
        self.password_raw = FakerClass().password()
        return super(AdminUserFactory, self).__init__(*args, **kwargs)
    class Meta:
        model = User
    
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True

    # email = Faker('email')
    # phone_number = Faker('phone_number')
    # category = Faker('random_element', elements=CATEGORIES_VALUES)

    # @post_generation
    # def password(self, create: bool, extracted: Sequence[Any], **kwargs):
    #     password = (
    #         extracted
    #         if extracted
    #         else self.password_raw
    #     )
    #     self.set_password(password)
    

class AdminUserFactory(django.DjangoModelFactory):

    def __init__(self, *args, **kwargs):
        self.password_raw = FakerClass().password()
        return super(AdminUserFactory, self).__init__(*args, **kwargs)

    class Meta:
        model = User
    
    email = Faker('email')
    is_superuser = True
    is_staff = True
    is_active = True
    password = PostGenerationMethodCall('set_password', 'password')

    # @post_generation
    # def password(self, create: bool, extracted: Sequence[Any], **kwargs):
    #     password = (
    #         extracted
    #         if extracted
    #         else self.password_raw
    #     )
    #     self.set_password(password)

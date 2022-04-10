from faker import Faker as FakerClass
from typing import Any, Sequence
from factory import django, Faker, post_generation
from account.models import User



class UserFactory(django.DjangoModelFactory):

    class Meta:
        model = User
    
    email = Faker('email')
    # email = Faker('email')
    # phone_number = Faker('phone_number')
    # category = Faker('random_element', elements=CATEGORIES_VALUES)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else FakerClass().password(
                length=30,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(password)

class AdminUserFactory(django.DjangoModelFactory):

    class Meta:
        model = User
    
    email = Faker('email')
    is_superuser = True
    is_staff = True
    # email = Faker('email')
    # phone_number = Faker('phone_number')
    # category = Faker('random_element', elements=CATEGORIES_VALUES)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else FakerClass().password(
                length=30,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(password)
from django.conf import settings
from django.contrib.auth.hashers import make_password
from factory import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    email = 'test@byteorbit.com'
    full_name = 'test user'
    _PASSWORD = 'lol'
    password = make_password(_PASSWORD)

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email', )

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        obj._PASSWORD = cls._PASSWORD


class SuperUserFactory(UserFactory):
    email = 'admin.test@byteorbit.com'
    full_name = 'test admin user'
    is_superuser = True
    is_staff = True

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    REQUIRED_FIELDS = ()

    @classmethod
    def create(cls, username, password, **kwargs):
        user = cls(username=username, is_active=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

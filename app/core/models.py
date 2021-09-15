from django.db import models

from django.contrib.auth.models import AbstractBaseUser,\
    BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra):
        """ creates and saves new user """
        if not email:
            raise ValueError("email can't be empty")
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_super_user(self, email, password, **extra):
        """ creates Super User"""

        user = self.create_user(email, **extra)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ custom user model that supports email instead of username """

    def get_short_name(self):
        pass

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

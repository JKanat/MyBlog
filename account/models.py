from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is not provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def _create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        code = get_random_string(length=25,
                                 allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789#$%&')
        self.activation_code = code

    def __str__(self):
        return self.email

        """
        shirf
        1.hashlib.md5(self,email + str(self.id)).encode() -> hexdigest()
        2.get_random_string(50,allowed_char=['which symbols are allowed in this string'])
        3.UUID
        4.datetime.datetime.now() or time.time() + timestamp() 01.011976
        """
        import hashlib
        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code



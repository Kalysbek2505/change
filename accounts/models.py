from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError('Требуется электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.is_active = False
        user.send_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_field):
        if not email:
            raise ValueError('Требуется электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=8, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    

    def generate_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.activation_code = code
        self.save()

    
    def send_activation_code(self):
        from django.core.mail import send_mail
        self.generate_activation_code()
        activation_url = f'http://127.0.0.1:8000/accounts/activate/{self.activation_code}'
        message = f'Активируйте свой аккаунт, перейдя по этой ссылке {activation_url}'
        send_mail('Активировать аккаунт', message, 'change@gmail.com', [self.email])
        

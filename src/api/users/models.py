from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        if not username:
            raise ValueError('El nombre de usuario debe ser proporcionado')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email,
                                username,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    google_id = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class Session(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    generation_date = models.DateTimeField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f"Session for {self.user.username}"

    def check_expiration(self):
        if self.expiration_date <= timezone.now():
            self.active = False
            self.save()

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
)


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, gender=2, **extra_fields):
        '''
        Create and save a user with the given username, email, and password.
        '''
        if not email:
            # 이메일 입력 안했을 때 오류 던지기
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username,
                          gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must habe is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must habe is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True)

    username = models.CharField(verbose_name='username', max_length=30)
    gender = models.SmallIntegerField(
        verbose_name='gender', choices=GENDER_CHOICES)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'<{self.pk} {self.email}>'

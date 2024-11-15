from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Информация о пользователе
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True)
    phone = PhoneNumberField(blank=True, verbose_name="Телефон")
    country = CountryField(blank=True, verbose_name="Страна")
    is_active = models.BooleanField(verbose_name='Проверка активности', default=True)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('block_users', 'block users'),
            ('can_view_list_of_users', 'can view list of users')
        ]

    def __str__(self):
        return self.email
from django.contrib.auth.models import AbstractUser
from django.db import models


class Counterparty(models.Model):
    """
    Контрагенты.
    """
    name = models.CharField('Название',
                            max_length=150,
                            unique=True)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Пользователи.
    """

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    email = models.EmailField('Email',
                              unique=True)
    first_name = models.CharField('Имя',
                                  max_length=150)
    last_name = models.CharField('Фамилия',
                                 max_length=150)
    counterparty = models.ForeignKey(Counterparty,
                                     blank=True,
                                     null=True,
                                     on_delete=models.CASCADE,
                                     related_name='employees',
                                     verbose_name='Контрагент')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

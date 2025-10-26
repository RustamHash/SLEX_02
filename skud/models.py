from django.db import models
from base_app.models import Filial


class SkudUser(models.Model):
    last_name = models.CharField(max_length=155, verbose_name='Фамилия')
    first_name = models.CharField(max_length=155, verbose_name='Имя')
    patronymic = models.CharField(max_length=155, verbose_name='Отчество')
    full_name = models.CharField(max_length=155, verbose_name='ФИО')

    def __str__(self):
        return f'{self.last_name}.{self.first_name[0].upper()}{self.patronymic[0].upper()}'

    class Meta:
        ordering = ('last_name', 'first_name', 'patronymic')
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class DataSkud(models.Model):
    full_name = models.CharField(max_length=155, verbose_name='Сотрудник')
    getting_started = models.DateField()
    end_of_work = models.DateField()
    type_direction = models.CharField(max_length=155, verbose_name='Направление')
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, verbose_name='Филиал', related_name='data_skud_filial')

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('filial', 'full_name')
        verbose_name = 'Данные Скуд'
        verbose_name_plural = 'Данные Скуд'

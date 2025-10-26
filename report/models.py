from django.db import models
from django.urls import reverse_lazy


class Reports(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    path_saved_reports = models.CharField(
        max_length=255, verbose_name="Папка сохранения отчетов"
    )
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy(f"reports-detail: {self.slug}")

    def get_home_url(self):
        return reverse_lazy(f"reports:{self.slug}")

    class Meta:
        ordering = ("position",)
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

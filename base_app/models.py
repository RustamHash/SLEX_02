from django.db import models
from django.urls import reverse_lazy


class Filial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    position = models.IntegerField(default=0)
    as_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('filial-detail', kwargs={'slug': self.slug})

    def get_home_url(self):
        return reverse_lazy(f'{self.slug}:home')

    class Meta:
        ordering = ('position',)
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

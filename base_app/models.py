from django.db import models
from django.urls import reverse_lazy


class Filial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    dsn = models.CharField(max_length=255)
    prog_id = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    as_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('filial-detail', kwargs={'slug': self.slug})

    def get_home_url(self):
        return reverse_lazy(f'main_filial', kwargs={'_filial_slug': self.slug})

    class Meta:
        ordering = ('position',)
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='menus')
    slug = models.SlugField()
    position = models.IntegerField(default=0)
    as_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('menu-detail', kwargs={'slug': self.slug})

    def get_home_url(self):
        return reverse_lazy(f'{self.slug}', kwargs={'_filial_slug': self.filial.slug})

    class Meta:
        ordering = ('position',)
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class Contracts(models.Model):
    id = models.AutoField(primary_key=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='contracts')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    path_saved_order = models.CharField(max_length=255)
    position = models.IntegerField(default=0)
    as_active = models.BooleanField(default=True)
    path_saved_reports = models.CharField(max_length=255)
    id_groups_goods = models.IntegerField(default=0)
    id_groups_vod = models.IntegerField(default=0)
    id_groups_vod_tls = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('contract-detail', kwargs={'slug': self.slug})

    def get_home_url(self):
        return reverse_lazy(f'detail_contract', kwargs={'_contract_slug': self.slug, '_filial_slug': self.filial.slug})

    def load_file_url(self):
        return reverse_lazy(f'load_file', kwargs={'_filial_slug': self.filial.slug, '_contract_slug': self.slug})

    class Meta:
        ordering = ('position',)
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

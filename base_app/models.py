from django.db import models
from django.urls import reverse_lazy


class Filial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    url_pg = models.CharField(max_length=255, verbose_name="Строка подключения к PG")
    url_wms = models.CharField(max_length=255, verbose_name="Строка подключения к WMS")
    login_wms = models.CharField(max_length=255, verbose_name="Логин WMS")
    password_wms = models.CharField(max_length=255, verbose_name="Пароль WMS")
    prog_id = models.IntegerField(default=0, verbose_name="Код программы Логистика")
    path_skud = models.CharField(max_length=255, verbose_name="Путь к папке скуд для филиала")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

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
    name = models.CharField(max_length=255, verbose_name="Наименование")
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='menus', verbose_name="Филиал")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

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
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='contracts', verbose_name="Филиал")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    path_saved_order = models.CharField(max_length=255, verbose_name="Папка сохранения заявок XML")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")
    path_saved_reports = models.CharField(max_length=255, verbose_name="Папка сохранения отчетов")
    id_groups_goods = models.IntegerField(default=0, verbose_name="Код папки товаров")
    id_groups_vod = models.IntegerField(default=0, verbose_name="Код папки водителей, для ОК")
    id_groups_vod_tls = models.IntegerField(default=0, verbose_name="Код папки водителей ТЛС, для ОК")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('operations-detail', kwargs={'slug': self.slug})

    def get_home_url(self):
        return reverse_lazy(f'operations', kwargs={'_contract_slug': self.slug, '_filial_slug': self.filial.slug})

    def handler_form(self):
        return reverse_lazy(f'handler_form', kwargs={'_filial_slug': self.filial.slug, '_contract_slug': self.slug})

    class Meta:
        ordering = ('position',)
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'


class Operations(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ManyToManyField(Contracts, related_name='operations', verbose_name="Контракт")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    load_file = models.BooleanField(default=True, verbose_name="Форма загрузки заявки")
    load_stock = models.BooleanField(default=True, verbose_name="Форма загрузки остатков")
    search_goods = models.BooleanField(default=True, verbose_name="Форма проверки товара в сетевом")
    btn_label = models.CharField(max_length=155, verbose_name="Надпись на кнопке")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('operations-detail', kwargs={'slug': self.slug})

    def get_home_url(self):
        return reverse_lazy('choice_operation', kwargs={
            # '_filial_slug': None,
            # '_contract_slug': None,
            '_operation_slug': self.slug
        })

    class Meta:
        ordering = ('position',)
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


class Reports(models.Model):
    id = models.AutoField(primary_key=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='reports', verbose_name="Филиал")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, verbose_name="URL")
    path_saved_reports = models.CharField(max_length=255, verbose_name="Папка сохранения отчетов")
    position = models.IntegerField(default=0, verbose_name="Позиция в меню")
    as_active = models.BooleanField(default=True, verbose_name="Признак активности")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('reports-detail', kwargs={'_report_slug': self.slug})

    def get_home_url(self):
        return reverse_lazy('reports', kwargs={'_filial_slug': self.filial.slug})

    class Meta:
        ordering = ('position',)
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

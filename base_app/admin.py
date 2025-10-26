from django.contrib import admin
from django.forms import TextInput
from django.db import models
from base_app.models import Filial, Menu, Contracts, Operations, Reports


class FilialAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Filial
        fields = '__all__'


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Menu
        fields = '__all__'


class ContractsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'filial')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['filial', 'name']
    list_filter = ('as_active',)
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size': '20'})},
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }
    class Meta:
        model = Contracts
        fields = '__all__'


class OperationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Operations
        fields = '__all__'


class ReportsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Reports
        fields = '__all__'


admin.site.register(Filial, FilialAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Contracts, ContractsAdmin)
admin.site.register(Operations, OperationAdmin)
admin.site.register(Reports, ReportsAdmin)

from django.contrib import admin
from base_app.models import Filial, Menu, Contracts


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
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Contracts
        fields = '__all__'


admin.site.register(Filial, FilialAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Contracts, ContractsAdmin)

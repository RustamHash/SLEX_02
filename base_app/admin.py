from django.contrib import admin
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
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

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

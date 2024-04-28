from django.contrib import admin
from base_app.models import Filial


class FilialAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Filial
        fields = '__all__'


admin.site.register(Filial, FilialAdmin)

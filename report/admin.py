from django.contrib import admin

from report.models import Reports


class ReportsAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Reports
        fields = "__all__"


admin.site.register(Reports, ReportsAdmin)

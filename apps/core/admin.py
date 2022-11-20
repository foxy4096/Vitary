from django.contrib import admin
from .models import Badge, Report


class ReportAdmin(admin.ModelAdmin):
    list_display = [
        "report_type",
        "url",
        "date",
    ]
    fields = [
        "report_type",
        "description",
        "url",
        "date",
        "user",
    ]
    readonly_fields = [
        "user",
        "date",
    ]


class BadgeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "color",
        "special",
    ]


admin.site.register(Badge, BadgeAdmin)
admin.site.register(Report, ReportAdmin)

admin.site.site_header = "Vitary Admin"
admin.site.site_title = "Vitary Admin"
admin.site.index_title = "Vitary Admin"

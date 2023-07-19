from django.contrib import admin

from apps.core.models import Badge, Report, Document


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
    search_fields = [
        "name",
        "description",
        "color",
    ]


class DocumentAdmin(admin.ModelAdmin):
    """Admin View for Document"""

    list_display = ("id", "file", "file_type", "file_url")
    list_filter = ("file_type",)
    fields = (
        "file",
        "file_type",
        "file_url",
    )
    readonly_fields = ("file_url",)


admin.site.register(Badge, BadgeAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Document, DocumentAdmin)

admin.site.site_header = "Vitary Administrative Dashboard"
admin.site.site_title = "Vitary Administrative Dashboard"
admin.site.index_title = "Vitary Administrative Dashboard"

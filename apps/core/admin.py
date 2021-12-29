from django.contrib import admin
from .models import Abuse

class AbuseAdmin(admin.ModelAdmin):
    list_display = ['user', 'abuse_type', 'description', 'date', 'to_vit']
    readonly_fields = ['user', 'abuse_type', 'description', 'date', 'to_vit']


admin.site.register(Abuse, AbuseAdmin)

admin.site.site_header = 'Vitary Admin'
admin.site.site_title = 'Vitary Admin'
admin.site.index_title = 'Vitary Admin'

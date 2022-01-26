from django.contrib import admin
from .models import Abuse, Badge, Requirments, Donation

class AbuseAdmin(admin.ModelAdmin):
    list_display = ['user', 'abuse_type', 'description', 'date', 'to_vit']
    readonly_fields = ['user', 'abuse_type', 'description', 'date', 'to_vit']

class RequirmenetsAdmin(admin.TabularInline):
    model = Requirments
    list_display = ['name', 'description', 'badge']
    extra = 3

class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'color', 'special']
    inlines = [RequirmenetsAdmin]

class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'amount']


admin.site.register(Abuse, AbuseAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Donation, DonationAdmin)

admin.site.site_header = 'Vitary Admin'
admin.site.site_title = 'Vitary Admin'
admin.site.index_title = 'Vitary Admin'

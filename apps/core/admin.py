from django.contrib import admin
from .models import Abuse, Badge, Requirments, Donation, DonationProof, BadgeRequest

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

# Approve the donation
def approve_donation(self, request, queryset):
    for donation in queryset:
        donation.approved = True
        donation.save()

# Approve the badge request
def approve_badge_request(self, request, queryset):
    for badge_request in queryset:
        badge_request.approved = True
        badge_request.save()


class DonationProofAdmin(admin.ModelAdmin):
    list_display = ['donation', 'proof']
    action = [approve_donation]

class BadgeRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'date', 'approved']
    action = [approve_badge_request]


admin.site.register(Abuse, AbuseAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationProof, DonationProofAdmin)
admin.site.register(BadgeRequest, BadgeRequestAdmin)

admin.site.site_header = 'Vitary Admin'
admin.site.site_title = 'Vitary Admin'
admin.site.index_title = 'Vitary Admin'

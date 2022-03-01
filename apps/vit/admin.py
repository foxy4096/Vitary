from django.contrib import admin

from .models import Vit, Plustag

class VitAdmin(admin.ModelAdmin):
    list_display = ['body', 'user', 'image', 'video', 'like_count', 'date']
    list_per_page = 10
    readonly_fields = ['user', 'likes', 'like_count', 'date']

class PlustagAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating']
    list_per_page = 10


admin.site.register(Vit, VitAdmin)
admin.site.register(Plustag, PlustagAdmin)

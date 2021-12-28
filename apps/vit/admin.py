from django.contrib import admin

from .models import Vit, Plustag

class VitAdmin(admin.ModelAdmin):
    list_display = ['body', 'user', 'image', 'video', 'like_count', 'date', 'to_reply_vits']
    readonly_fields = ['user', 'likes', 'like_count', 'date']


admin.site.register(Vit, VitAdmin)
admin.site.register(Plustag)
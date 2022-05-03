from django.contrib import admin

from .models import Vit, Plustag, Comment

class PlustagAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating']
    list_filter = ['name', 'rating']
    search_fields = ['name']
    list_per_page = 10

class CommentAdmin(admin.TabularInline):
    readonly_fields = ['body','user', 'vit', 'date']
    extra = 0
    model = Comment

class VitAdmin(admin.ModelAdmin):
    list_display = ['body', 'user', 'image', 'video', 'like_count', 'date']
    inlines = [CommentAdmin]
    list_filter = ['user', 'date']
    search_fields = ['body']
    list_per_page = 10
    readonly_fields = ['user', 'likes', 'like_count', 'mentions', 'plustag', 'date',]

admin.site.register(Vit, VitAdmin)
admin.site.register(Plustag, PlustagAdmin)
from django.contrib import admin

# Register your models here.
from .models import DevProfile, DocumentationCategory, Documentation, Bot
class DocumentationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'description', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'content', 'description')

class DocumentationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    list_per_page = 10
    verbose_name_plural = 'Documentation Categories'

class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'user', 'owner')
    list_per_page = 10
    fields = ('name', 'description', 'user', 'owner', 'endpoint', 'private_key')
    readonly_fields = ('user', 'owner', 'private_key')

admin.site.register(Bot, BotAdmin)
admin.site.register(DocumentationCategory, DocumentationCategoryAdmin)
admin.site.register(Documentation, DocumentationAdmin)
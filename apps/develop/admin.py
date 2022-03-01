from django.contrib import admin

# Register your models here.
from .models import DevProfile, DocumentationCategory, Documentation

class DocumentationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(DocumentationCategory, DocumentationCategoryAdmin)
admin.site.register(Documentation, DocumentationAdmin)
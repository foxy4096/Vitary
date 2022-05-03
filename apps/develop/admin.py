from django.contrib import admin

# Register your models here.
from .models import DevProfile, DocumentationCategory, Documentation
class DocumentationAdmin(admin.StackedInline):
    model = Documentation
    prepopulated_fields = {'slug': ('title',)}


class DocumentationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [DocumentationAdmin]
    search_fields = ('name',)
    fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    list_per_page = 10
    verbose_name_plural = 'Documentation Categories'

admin.site.register(DocumentationCategory, DocumentationCategoryAdmin)
# admin.site.register(Documentation, DocumentationAdmin)
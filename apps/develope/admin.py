from django.contrib import admin

from .models import DevProfile, DocumentationTag, Documentation


class DevProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'twitter_handle',
                    'github_handle', 'linkedin_handle')


class DocumentationTagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DocumentationAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'tag', 'slug')
    readonly_fields = ('slug',)
    list_display = ('title', 'created_at', 'updated_at', 'tag')

    search_fields = ('title', 'description', 'tag')

    list_filter = ('created_at', 'updated_at', 'tag')


admin.site.register(DevProfile, DevProfileAdmin)
admin.site.register(DocumentationTag, DocumentationTagAdmin)
admin.site.register(Documentation, DocumentationAdmin)

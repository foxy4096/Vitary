from django.contrib import admin

from .models import Feed, FeedComment

class FeedAdmin(admin.ModelAdmin):
    list_display = ['body', 'created_by', 'image', 'video',]
    readonly_fields = ['created_by', 'likes']


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedComment)
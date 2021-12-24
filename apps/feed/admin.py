from django.contrib import admin

from .models import Feed, FeedComment

class FeedAdmin(admin.ModelAdmin):
    list_display = ['body', 'user', 'image', 'video', 'like_count', 'date']
    readonly_fields = ['user', 'likes', 'like_count', 'date']


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedComment)
from django.contrib import admin

from .models import Feed, FeedComment

class FeedAdmin(admin.ModelAdmin):
    list_display = ['body', 'user', 'image', 'video',]
    readonly_fields = ['user', 'likes']


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedComment)
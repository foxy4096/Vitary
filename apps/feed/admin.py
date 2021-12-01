from django.contrib import admin

from .models import Feed, FeedComment

admin.site.register(Feed)
admin.site.register(FeedComment)
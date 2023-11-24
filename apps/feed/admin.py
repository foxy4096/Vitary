from django.contrib import admin

from .models import Feed, Plustag, Comment


class PlustagAdmin(admin.ModelAdmin):
    list_display = ["name", "rating"]
    list_filter = ["name", "rating"]
    search_fields = ["name"]
    list_per_page = 10


class CommentAdmin(admin.ModelAdmin):
    list_display = ["body", "user", "feed", "date"]
    fields = ["body", "user", "feed", "date", "reply_to"]
    readonly_fields = ["user", "feed", "date"]

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ["body", "user", "like_count", "date"]
    list_filter = ["user", "date"]
    search_fields = ["body"]
    autocomplete_fields = ["user", "plustag", "mentions", "likes"]
    list_per_page = 10
    readonly_fields = [
        "like_count",
        "date",
    ]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Plustag, PlustagAdmin)
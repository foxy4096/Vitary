from django.contrib import admin

from .models import Vit, Plustag, Comment, Embed


class PlustagAdmin(admin.ModelAdmin):
    list_display = ["name", "rating"]
    list_filter = ["name", "rating"]
    search_fields = ["name"]
    list_per_page = 10


class CommentAdmin(admin.ModelAdmin):
    list_display = ["body", "user", "vit", "date"]
    fields = ["body", "user", "vit", "date", "reply_to"]
    readonly_fields = ["user", "vit", "date"]

@admin.register(Embed)
class EmbedAdmin(admin.ModelAdmin):
    fields = ["url", "vit", "title", "description", "image_url", "video_url"]
    readonly_fields = ["vit"]


@admin.register(Vit)
class VitAdmin(admin.ModelAdmin):
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
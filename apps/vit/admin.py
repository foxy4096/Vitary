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


class EmbedAdmin(admin.TabularInline):
    fields = ["url", "vit", "title", "description", "image_url", "video_url"]
    readonly_fields = ["vit"]
    extra = 0
    model = Embed


class VitAdmin(admin.ModelAdmin):
    list_display = ["body", "user", "like_count", "date"]
    inlines = [EmbedAdmin]
    list_filter = ["user", "date"]
    search_fields = ["body"]
    list_per_page = 10
    readonly_fields = [
        "user",
        "likes",
        "like_count",
        "mentions",
        "plustag",
        "contain_embed",
        "saved_embed",
        "plustag",
        "date",
    ]


admin.site.register(Vit, VitAdmin)
admin.site.register(Embed)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Plustag, PlustagAdmin)
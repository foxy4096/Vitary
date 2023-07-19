from django.contrib import admin
from .models import ChatMessage, Chat


class ChatMessageAdmin(admin.TabularInline):
    model = ChatMessage
    fields = ("message", "created_by", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ["created_by"]
    extra = 1


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = [ChatMessageAdmin]
    list_display = ["id", "__str__"]
    readonly_fields = ["modified_at"]
    list_filter = ["modified_at"]
    search_fields = ["message"]
    autocomplete_fields = ["users"]

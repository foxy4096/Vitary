from django.contrib import admin

from apps.core.models import Comment

admin.site.site_header = 'Vitary Admin'
admin.site.site_title = 'Vitary Admin'
admin.site.index_title = 'Vitary Admin'


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['comment', 'created_by']
    can_delete = False
    extra = 1

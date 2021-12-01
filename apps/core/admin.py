from django.contrib import admin

from apps.core.models import Issue, Comment

admin.site.site_header = 'Vitary Admin'
admin.site.site_title = 'Vitary Admin'
admin.site.index_title = 'Vitary Admin'


class CommentInline(admin.TabularInline):
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.profile
        return super().save_model(request, obj, form, change)

    model = Comment
    fields = ['comment', 'created_by']
    can_delete = False
    extra = 1


class IssueAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ]


admin.site.register(Issue, IssueAdmin)

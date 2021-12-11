from django.contrib import admin

from apps.blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'user')
    exclude = ('slug', 'user') 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user.profile)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user.profile
        return super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
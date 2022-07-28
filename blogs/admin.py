from django.contrib import admin
from blogs.models import Posts


# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'is_public', 'total_likes']
    list_editable = ['is_public']


admin.site.register(Posts, PostsAdmin)

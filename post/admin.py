from django.contrib import admin
from post.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ["id","timestamp","update","title","slug"]
    list_filter = ["id","timestamp","content"]
    list_editable = ["title"]
    search_fields = ["update","content"]

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)

from django.contrib import admin
from django.contrib.admin.filters import ListFilter

from .models import Post, Author, Tag, Comments
# Register your models here.

#to organize admin/blog/post/ : columns, filters
class PostAdmin(admin.ModelAdmin):
    #filters
    list_filter = ("author", "tags", "date",)
    #colunmns 
    list_display = ("title", "date", "author",)
    #have the slug automaticaly fullfield 
    prepopulated_fields = {"slug": ("title",)}

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post", "body")

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comments, CommentsAdmin)
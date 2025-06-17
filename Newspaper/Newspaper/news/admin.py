from django.contrib import admin
from .models import Post, Comment, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_type', 'author', 'title', 'rating')
    list_filter = ('post_type', 'author', 'category')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_date', 'rating')
    list_filter = ('user', 'post', 'comment_date')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    list_filter = ('category_name',)


# Register your models her
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)

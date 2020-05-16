from django.contrib import admin

from .models import Post, Tag, Comment
# Register your models here.


admin.site.register(Tag)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'date_pub')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_pub')
    exclude = ('slug',)
    list_filter = ('date_pub',)
    inlines = [CommentInline]

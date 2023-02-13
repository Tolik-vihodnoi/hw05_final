from django.contrib import admin

from .models import Group, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date',
                    'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_editable = ('group',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('slug', 'title')
    list_filter = ('title',)
    empty_value_display = '-пусто-'
    list_display_links = ('slug',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created')
    search_fields = ('text', 'author', 'created')
    list_filter = ('author', 'post', 'created')
    empty_value_display = '-пусто-'
    list_display_links = ('text',)
    list_editable = ('author',)
    list_select_related = ('author',)
    ordering = ('post',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)

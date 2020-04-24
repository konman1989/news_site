from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment


class PostAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'created_on')
    list_filter = ("author", "status")
    search_fields = ['title', 'content', 'author__email']
    actions = ['move_to_pending', 'approve_posts', 'decline_posts']
    prepopulated_fields = {'content': ('title',)}
    summernote_fields = ('content',)

    def move_to_pending(self, request, queryset):
        queryset.update(status=0)

    def approve_posts(self, request, queryset):
        queryset.update(status=1)

    def decline_posts(self, request, queryset):
        queryset.update(status=2)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'author', 'email', 'created_on')
    search_fields = ['content', 'email', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

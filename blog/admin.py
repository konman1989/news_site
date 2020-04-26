from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'created_on')
    list_filter = ("author", "status")
    search_fields = ['title', 'content', 'author__email']
    actions = ['move_to_pending', 'approve', 'decline']
    prepopulated_fields = {'content': ('title',)}
    summernote_fields = ('content',)

    def move_to_pending(self, request, queryset):
        queryset.update(status=0)

    def approve(self, request, queryset):
        queryset.update(status=1)

    def decline(self, request, queryset):
        queryset.update(status=2)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'author', 'email', 'created_on')
    search_fields = ['content', 'email', 'author']




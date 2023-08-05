from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models

admin.site.site_header = "Todo Admin"
admin.site.index_title = "Admin"


@admin.register(models.TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    actions = ['complete_selected']
    list_display = ['id', "title", 'is_complete', 'created_at', 'due_date', 'username', 'do_now']
    list_editable = ['due_date']
    list_per_page = 20
    list_select_related = ['user']
    ordering = ['id', 'title']

    def username(self, todoitem):
        url = (
                reverse('admin:todoV1_todoitem_changelist')
                + '?'
                + urlencode({'user__id': str(todoitem.user.id)})
        )
        return format_html('<a href="{}">{}</a>', url, todoitem.user.username)

    @admin.display(ordering='due_date')
    def do_now(self, todoitem):
        if todoitem.due_date > todoitem.created_at.date():
            return 'Do Now'
        else:
            return "Ok"

    def complete_selected(self, request, queryset):
        update_count = queryset.update(is_complete=1)
        self.message_user(
            request,
            f'{update_count} items is set to Completed'
        )


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'todo_count']
    list_per_page = 15
    list_editable = ['email']
    ordering = ['id', 'username']
    search_fields = ['username__startswith']

    @admin.display(ordering='todo_count')
    def todo_count(self, user):
        url = (
                reverse('admin:todoV1_todoitem_changelist')
                + '?'
                + urlencode({'user__id': str(user.id)})
        )
        return format_html('<a href="{}">{}</a>', url, user.todo_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(todo_count=Count('todoitem'))
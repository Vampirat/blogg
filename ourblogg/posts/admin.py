from django.contrib import admin
from .models import PostsModel, CommentsModel


@admin.register(PostsModel)
class PostsAdmin(admin.ModelAdmin):

    list_display = ('pk', 'title', 'is_published', 'date_create', 'date_update', 'user_id', 'tag_list', )
    ordering = ['pk', 'is_published', 'title', 'date_create']
    list_editable = ('is_published', )
    list_filter = ['is_published', 'date_create', ]
    actions = ['not_published', 'for_published']

    #чтобы отображать теги в админке
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    
    @admin.action(description='Сделать выбранные посты "Не для публикации"')
    def not_published(self, request, quaryset):
        count = quaryset.update(is_published=False)
        self.message_user(request, f'Вы изменили {count} записей')
    
    @admin.action(description='Сделать выбранные посты "Для публикации"')
    def for_published(self, request, quaryset):
        count = quaryset.update(is_published=True)
        self.message_user(request, f'Вы изменили {count} записей')

@admin.register(CommentsModel)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['body', 'date_create', 'active', 'user', 'post']
    list_editable = ('active', )

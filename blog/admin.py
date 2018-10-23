from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                    'status')
    # 添加右边栏的过滤器
    list_filter = ('status', 'created', 'publish', 'author')
    # 搜索框
    search_fields = ('title', 'body')
    # 通过使用prepopulated_fields属性告诉Django通过输入的标题来填充slug字段
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('author',)
    # 产生在搜索框下一个通过时间层快速导航的栏
    date_hierarchy = 'publish'
    # 设置这些帖子的默认排列顺序
    ordering = ['status', 'publish']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'blody')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)


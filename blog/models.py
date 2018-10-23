from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from DjangoUeditor.models import UEditorField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(
                            User,
                            on_delete=models.CASCADE,
                            related_name='blog_posts')
    # 为博客帖子添加图片
    image = models.ImageField(upload_to='blog/%Y/%m/%d',
                              blank=True)

    # body = models.TextField()
    body = UEditorField(width=600, height=300, toolbars="full",
                        imagePath='img/', filePath='files/',
                        upload_settings={"imageMaxSize": 1204000},
                        settings={}, verbose_name='正文')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager
    # 添加标签
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    class Meta:
        ordering = ('-publish', )
        verbose_name = '帖子'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    # 使用外键ForeignKey 定义多对一关系， 因为每一条评论只能在一个帖子下生成，
    # 而每一个帖子又可能包含多个评论
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        # 以创建时间排序
        ordering = ('created', )
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


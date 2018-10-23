from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # IF page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # IF page is out of range deliver last og result
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        #  A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #  Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            #  save the comment to the database
            new_comment.save()
    else:
            comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    # 对结果进行分页处理每页只显示3个对象
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    # 如果我们得到一个GET请求， 一个空的表单必须显示，而如果我们得到一个POST请求，则表单需要提交和处理。
    # 因此，我们使用request.method == 'POST'来区分这两种场景
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        # 验证引进的数据是否有效，有效则返回True，无效则返回False
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(
                                    post.get_absolute_url())
            subject = '{} ({}) recommands you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'],
                                                                    cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})

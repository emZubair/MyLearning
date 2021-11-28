from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from taggit.models import Tag

from .models import Post
from .helpers import send_email
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.publisher.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None, *args, **kwargs):  # pylint-ignore=unused-variables
    posts = Post.publisher.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:    # DEFAULT TO First Page when no page number is specified
        posts = paginator.page(1)
    except EmptyPage:   # If page is out of range, Display the last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page_number,
                                                   'tag_slug': tag_slug})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', published__year=year,
                             published__month=month, published__day=day)

    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.objects.filter(tags__in=post_tags_ids, status='published').exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('same_tags', '-published')[:4]
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'related_posts': related_posts})


def default_pager(request, msg):

    return render(request, 'blog/post/temp.html', {'message': msg})


def share_post(request, post_id):
    """
    get post by id and share by Email
    :param request: (HttpRequest)
    :param post_id: (str)
    :return:
    """

    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            sent = send_email(request, post, cleaned_data)
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post, 'form': form, 'sent': sent
    })

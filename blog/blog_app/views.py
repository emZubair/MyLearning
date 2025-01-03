from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from taggit.models import Tag

from .models import Post, Contact
from .helpers import send_email
from blog.actions.utils import create_action
from common.decorators import ajax_required
from common.utils import get_redis_connector
from .forms import (EmailPostForm, CommentForm, SearchForm)


redis = get_redis_connector()


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
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'blog/post.ajax_list', {
            'posts': posts
        })
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page_number,
                                                   'tag_slug': tag_slug})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', published__year=year,
                             published__month=month, published__day=day)

    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.objects.filter(tags__in=post_tags_ids, status='published').exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('same_tags', '-published')[:4]
    # Store post View count & ranking set in redis
    total_views = redis.incr(f'post:{post.id}:views')
    redis.zincrby('post_ranking', 1, post.id)
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
                                                     'total_views': total_views,
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
            create_action(request.user, 'Shared a post via Email', post)
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post, 'form': form, 'sent': sent
    })


def post_search(request):

    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_query = SearchQuery(query)
            # search_vector = SearchVector('title', 'body')
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            # results = Post.publisher.annotate(
            #     search=search_vector, rank=SearchRank(search_vector, search_query)).filter(
            #     rank__gte=0.3).order_by('-rank')
            results = Post.publisher.annotate(similarity=TrigramSimilarity('title', query)).filter(
                similarity__gt=0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html', {
        'form': form, 'query': query, 'results': results
    })


@login_required
@require_POST
@ajax_required
def like_post(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')

    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            post.increment_likes() if action == 'like' else post.decrement_likes()
            post.save()
            create_action(request.user, 'Liked a post', post)

            return JsonResponse({'status': 'Ok', 'count': post.likes})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def list_users(request):
    users = User.objects.all()
    return render(request, 'blog/post/list_users.html', {'users': users})


@login_required
def user_details(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'blog/post/user_details.html', {'user': user})


@login_required
@ajax_required
@require_POST
def follow_user(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)

            if action == 'follow':
                Contact.objects.get_or_create(from_user=request.user, to_user=user)
                create_action(request.user, 'Followed', user)
            else:
                Contact.objects.filter(from_user=request.user, to_user=user).delete()
                create_action(request.user, 'unfollowed', user)
            return JsonResponse({'status': 'Ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


@login_required
def popular_posts(request):
    # Get post ranking dict
    post_rankings = redis.zrange('post_ranking', 0, -1, desc=True)[:5]
    post_ranking_ids = [int(id) for id in post_rankings]
    popular_post = list(Post.objects.filter(id__in=post_ranking_ids))
    popular_post.sort(key=lambda x: post_ranking_ids.index(x.id))
    return render(request, 'blog/post/popular.html', {
        'popular_posts': popular_post
    })

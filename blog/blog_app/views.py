from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post


def post_list(request, *args, **kwargs):  # pylint-ignore=unused-variables
    posts = Post.publisher.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:    # DEFAULT TO First Page when no page number is specified
        posts = paginator.page(1)
    except EmptyPage:   # If page is out of range, Display the last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page_number})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', published__year=year,
                             published__month=month, published__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def default_pager(request, msg):

    return render(request, 'blog/post/temp.html', {'message': msg})

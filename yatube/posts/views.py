from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator

from .models import Post, Group, User

from django.contrib.auth.decorators import login_required

from .forms import PostForm

POST = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # В словаре context отправляем информацию в шаблон
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:POST]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    count = Post.objects.filter(author__username=username).count()
    posts = Post.objects.filter(author__username=username)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'count': count,
        'page_obj': page_obj,
        'author': User,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    group = post.group
    author = post.author
    posts = Post.objects.all()
    count = Post.objects.filter(author=author).count()
    context = {
        'post': post,
        'author': author,
        'group': group,
        'posts': posts,
        'count': count
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)
    else:
        form = PostForm()
        return render(request, template, {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:profile', request.user.username)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.pk)
    else:
        form = PostForm(instance=post)
        context = {
            'is_edit': True,
            'post': post,
            'form': form
        }
        return render(request, 'posts/create_post.html', context)

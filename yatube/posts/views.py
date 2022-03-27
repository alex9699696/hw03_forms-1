from gettext import install
from re import template
import re
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User

MAX_POST = 10


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, MAX_POST) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    #posts = Post.objects.order_by('-pub_date')[:MAX_POST]
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, MAX_POST) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    template = 'posts/group_list.html'
    #posts = Post.objects.filter(group=group).order_by('-pub_date')[:MAX_POST]
    context = {
        'title': group.title,
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required    
def profile(request, username):
    author = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    paginator = Paginator(user_posts, MAX_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'author' : author
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post_id = get_object_or_404(Post, pk=post_id)
    template = 'posts/post_detail.html'
    group = post_id.group
    posts = Post.objects.count()
    context = {
            'author' : post.author
    }
    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'
    title = 'Новый пост'
    context = {
        'title': title,
    }
    if request.method == 'POST'
        form = PostForm(request.Post)
        context.update = {'form': form}
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/profile/,<username>')
        else:
            return render(request, template, context)
    else:
        form = Postform()
        return render(request, template, context)

@login_required
def post_create(request):
    form = PostForm('text', 'group')
    template = 'posts/create_post.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('post:profile', post = post)
    form = Postform(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post:profile', request.user.username)
    else:
        form = PostForm(instance=post)
        template = 'posts/create_post.html'
        context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
        return render(request, template, context)
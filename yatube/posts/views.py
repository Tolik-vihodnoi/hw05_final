from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utils import do_page_obj


def index(request):
    posts = Post.objects.select_related('author',
                                        'group')
    page_obj = do_page_obj(request, posts, settings.NUM_OF_POSTS)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author', 'group')
    page_obj = do_page_obj(request, posts, settings.NUM_OF_POSTS)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    posts_owner = get_object_or_404(User, username=username)
    posts = posts_owner.posts.select_related('author', 'group')
    page_obj = do_page_obj(request, posts, settings.NUM_OF_POSTS)
    user = request.user
    following = (
            user.is_authenticated
            and not user == posts_owner
            and Follow.objects.filter(user=user, author=posts_owner).exists()
    )
    context = {
        'page_obj': page_obj,
        'posts_owner': posts_owner,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'group'),
        pk=post_id
    )
    form = CommentForm()
    comments = post.comments.select_related('author')
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    save_form = form.save(commit=False)
    save_form.author = request.user
    save_form.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post_obj = get_object_or_404(Post, id=post_id)
    if request.user != post_obj.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        instance=post_obj,
        files=request.FILES or None
    )
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form,
                                                          'post_id': post_id})
    form.save()
    return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id)


@login_required
def follow_index(request):
    follower = request.user
    posts = Post.objects.filter(
        author__following__user=follower).select_related('group', 'author')
    page_obj = do_page_obj(request, posts, settings.NUM_OF_POSTS)
    context = {'page_obj': page_obj}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    user = request.user
    if user != get_object_or_404(User, username=username):
        author = get_object_or_404(User, username=username)
        data = {
            'user': user,
            'author': author
        }
        Follow.objects.get_or_create(**data)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    data = {
        'user': user,
        'author': author
    }
    Follow.objects.filter(**data).delete()
    return redirect('posts:profile', username)

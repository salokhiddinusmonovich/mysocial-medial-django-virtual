from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests import Response
from .forms import *
from a_posts.models import *
from django.db.models import Count
from django import forms
from django.forms import ModelForm
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page', 1))
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('')

    context = {
        'posts': posts,
        'tag': tag,
        'page': page
    }

    if request.htmx:
        return render(request, 'snippets/loop_home_posts.html', context)

    return render(request, 'a_posts/home.html', context)


@login_required
def post_create_view(request):
    form = PostCreatForm()
    if request.method == 'POST':
        form = PostCreatForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            url = form.cleaned_data['url']

            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://www.pinterest.com/"
                }

                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    return HttpResponse(f"Request failed: status code {response.status_code}", content_type="text/plain")

                soup = BeautifulSoup(response.text, 'html.parser')

                # Извлечение изображения
                image_tag = soup.select_one('meta[property="og:image"]')
                post.image = image_tag['content'] if image_tag and 'content' in image_tag.attrs else None

                # Извлечение заголовка / описания
                title_tag = soup.select_one('meta[property="og:description"]')
                post.title = title_tag['content'].strip() if title_tag else 'Untitled'

                # Извлечение автора
                author_tag = soup.select_one('meta[name="pinterestapp:owner_name"]')
                post.artist = author_tag['content'].strip() if author_tag else 'Unknown'

                post.author = request.user

                post.save()
                form.save_m2m()

                messages.success(request, 'Post created successfully.')
                return redirect('home')

            except Exception as e:
                return HttpResponse(f"Error while parsing: {str(e)}", content_type="text/plain")

    return render(request, 'a_posts/post_create.html', {'form': form})




@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')

    return render(request, 'a_posts/post_delete.html', {'post': post})



@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk,author=request.user)
    form = PostEditForm(instance=post)
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated')
            return redirect('home')
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'a_posts/post_edit.html', context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreatForm()
    replyform = ReplyCreateForm
    categories = Tag.objects.all()

    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments, 'replyform': replyform})



    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform,
    }

    return render(request, 'a_posts/post_page.html', context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = CommentCreatForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            messages.success(request, 'You have just written a comment!')

    context = {
        'post': post,
        'comment': comment,
        'replyform': replyform
    }

    return render(request, 'snippets/add_comments.html', context)


@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {
        'reply': reply,
        'comment': comment,
        'replyform': replyform
    }

    return render(request, 'snippets/add_reply.html', context)

@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, 'Comment Deleted')
        return redirect('post', post.parent_post.id)

    return render(request, 'a_posts/comment_delete.html', {'comment': post})

@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == "POST":
        reply.delete()
        messages.success(request, 'Reply Deleted')
        return redirect('post', reply.parent_comment.parent_post.id)

    return render(request, 'a_posts/reply_delete.html', {'reply': reply})


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()

            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request, post)

        return wrapper

    return inner_func


@login_required
@like_toggle(Post)
def like_post(request, post):
    return render(request, 'snippets/likes.html', {'post' : post })


@login_required
@like_toggle(Comment)
def like_comment(request, post):
    return render(request, 'snippets/likes_comment.html', {'comment' : post })


@login_required
@like_toggle(Reply)
def like_reply(request, post):
    return render(request, 'snippets/likes_reply.html', {'reply' : post })


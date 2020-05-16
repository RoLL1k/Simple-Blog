from django.http import Http404, HttpResponseRedirect

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm, CommentForm

from django.db.models import Q


def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    return render(request, 'blog/index.html', context={'posts': posts})


class PostDetail(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug__iexact=slug)
        form = CommentForm(initial={'post': post})
        return render(request, 'blog/post_detail.html',
                      context={"post": post, 'form': form, 'admin_object': post, 'detail': True, })


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    model_url = 'posts_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    model_url = 'tags_list_url'
    raise_exception = True


def comment_create(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug__iexact=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_detail_url', slug=slug)
        return render(request, 'blog/post_detail.html',
                      context={"post": post, 'form': form, 'detail': True, })
    return redirect(request.META['HTTP_REFERER'])


def answer_create(request, slug, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_detail_url', slug=slug)
        return render(request, 'blog/answer_create.html', {"form": form})
    else:
        comment = get_object_or_404(Comment, id=id)
        form = CommentForm(initial={'comment': comment})
        return render(request, 'blog/answer_create.html', {"form": form})

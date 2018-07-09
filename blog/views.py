import os
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Post
from .forms import PostForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
# 쿼리 OR조건을 위해서 import 함 
from django.db.models import Q

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
    #posts = Post.objects.order_by('published_date')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(os.path.join(BASE_DIR, 'templates'))
    return render(request, 'blog/post_list.html', {'posts': posts})

class PagesView(TemplateView):
    '''객체형태로 page 목록을 출력함'''
    template_name = 'blog/pages.html'

    def get_context_data(self, **kwargs):
        context = super(PagesView, self).get_context_data(**kwargs)
        # 검색 조건 추가 시작 
        q = self.request.GET.get('q')
        if q : 
            posts = Post.objects.filter(Q(title__contains=q) |Q(text__contains=q) ).order_by('-id')
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
        context['q'] = q if q != None else ""
        context['q_str'] = 'q=' + q if q!= None else ""            
        # 검색조건 추가 종료
        paginator = Paginator(posts, 10)
        page = self.request.GET.get('page')
        try:
            show_posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            #show_posts = paginator.page(paginator.num_pages)
            show_posts = paginator.page(1)
        context['posts'] = show_posts
        return context

def post_page(request, pk=1):
    '''함수형태로 page 목록을 출력함'''
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
    paginator = Paginator(posts, 10) # Show 10 contacts per page
    page = pk
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_page.html', {'posts': posts })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
    #return render(request, 'blog/test.html',{'post': post })

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)            
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')

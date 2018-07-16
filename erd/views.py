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


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
    #posts = Post.objects.order_by('published_date')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(os.path.join(BASE_DIR, 'templates'))
    return render(request, 'blog/post_list.html', {'posts': posts})
from django.shortcuts import render
from django.views.generic import *

from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "post_list.html"


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"

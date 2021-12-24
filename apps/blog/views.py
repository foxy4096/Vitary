from django.shortcuts import render
from django.views.generic import *
from django.core.paginator import Paginator


from .models import Post

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, 'blog/post_list.html', {'posts': page_obj})

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"

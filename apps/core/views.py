from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from apps.feed.forms import FeedForm

from apps.feed.models import Feed


def redirect_to_home(request):
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        feeds = Feed.objects.filter(Q(user=request.user) | Q(
            user__profile__in=request.user.profile.follows.all()) | Q(user__profile__in=request.user.profile.followed_by.all())).order_by('-date')
        paginator = Paginator(feeds, 5)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)
        form = FeedForm()
        return render(request, 'core/home/home_logged_in.html', {'feeds': page_obj, 'form': form})
    else:
        return render(request, 'core/home/home_logged_out.html')


def peoples(request):
    persons = User.objects.all()
    return render(request, 'core/peoples.html', {'persons': persons})

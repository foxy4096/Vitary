from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from apps.vit.forms import VitForm

from apps.vit.models import Vit


def redirect_to_home(request):
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        vits = Vit.objects.filter(Q(user=request.user) | Q(
            user__profile__in=request.user.profile.follows.all()) | Q(user__profile__in=request.user.profile.followed_by.all())).order_by('-date')
        paginator = Paginator(vits, 5)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)
        form = VitForm()
        return render(request, 'core/home/home_logged_in.html', {'vits': page_obj, 'form': form})
    else:
        return render(request, 'core/home/home_logged_out.html')

def base_layout(request):
	template='core/base.html'
	return render(request,template)

def peoples(request):
    persons = User.objects.all()
    return render(request, 'core/peoples.html', {'persons': persons})

def explore(request):
    vits = vit.objects.all().order_by('-like_count', '-date')
    paginator = Paginator(vits, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    context = {
        'vits': page_obj,
    }
    return render(request, 'core/explore.html', context)
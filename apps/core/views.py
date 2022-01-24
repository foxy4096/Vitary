from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from apps.vit.forms import VitForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReportAbuseForm

from apps.vit.models import Vit, Comment, Plustag
from django.contrib.auth.models import User


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
        return render(request, 'core/home/home_logged_out.html', {'show': False})


def peoples(request):
    persons = User.objects.all().order_by('-date_joined')
    paginator = Paginator(persons, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, 'core/peoples.html', {'persons': page_obj})

def explore(request):
    vits = Vit.objects.all().order_by('-like_count', '-date')
    # paginator = Paginator(vits, 5)
    # page_no = request.GET.get('page')
    # page_obj = paginator.get_page(page_no)
    context = {
        'vits': vits,
    }
    return render(request, 'core/explore.html', context)


@login_required
def report_abuse(request, pk):
    if request.method == 'POST':
        form = ReportAbuseForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.to_vit = get_object_or_404(Vit, id=pk)
            report.user = request.user
            report.save()
            messages.success(request, 'Your report has been submitted successfully')
            return redirect('home')
    else:
        form = ReportAbuseForm()
    return render(request, 'core/report_abuse.html', {'form': form, 'vit': get_object_or_404(Vit, id=pk)})


def page_404(request):
    return render(request, '404.html')

def search(request):
    original_query = request.GET.get('q', '')
    query = original_query
    stype = request.GET.get('stype', '')
    if query != '':
        if query[0] == '@' and stype == '':
            stype = 'users'
        if query[0] != '@' and stype == '':
            stype = 'vits'
        if stype == 'vits':
            vits = Vit.objects.filter(Q(user__username__icontains=query) | Q(
                user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(
                body__icontains=query)).order_by('-date')
            paginator = Paginator(vits, 5)
            page_no = request.GET.get('page')
            page_obj = paginator.get_page(page_no)
            context = {
                'vits': page_obj,
                'stype': 'vits',
                'query': query,
            }
            return render(request, 'core/search.html', context)
        elif stype == 'users':
            query = query.replace('@', '')
            persons = User.objects.filter(Q(username__icontains=query) | Q(
                first_name__icontains=query) | Q(last_name__icontains=query)).order_by('-date_joined')
            paginator = Paginator(persons, 5)
            page_no = request.GET.get('page')
            page_obj = paginator.get_page(page_no)
            return render(request, 'core/search.html', {'persons': page_obj, 'stype': 'users', 'query': original_query})
        else:
            return redirect('home')
    else:
        return redirect('home')

    
def terms(request):
    return render(request, 'core/terms.html')
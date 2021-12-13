from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from apps.core.models import Issue, Comment
from apps.feed.models import Feed
from apps.core.forms import IssueForm

import os

def redirect_to_home(request):
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        feeds = Feed.objects.filter(Q(user=request.user) | Q(
            user__profile__in=request.user.profile.follows.all()) | Q(user__profile__in=request.user.profile.followed_by.all())).order_by('-date')
        paginator = Paginator(feeds, 5)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)
        return render(request, 'core/home/home_logged_in.html', {'feeds': page_obj})
    else:
        return render(request, 'core/home/home_logged_out.html')


def peoples(request):
    persons = User.objects.all()
    return render(request, 'core/peoples.html', {'persons': persons})


@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user.profile
            report.save()
            messages.success(request, '📩 Your Issue has been reported successfully and will be reviewed shortly by the admin team to resolve the issue as soon as possible!')
            return redirect('home')
    form = IssueForm()
    user_issues = Issue.objects.filter(user=request.user)
    all_issues = Issue.objects.all()
    return render(request, 'core/report_issue.html', {'form': form, 'issues': user_issues, 'all_issues': all_issues})

@login_required
def issue_detail(request, pk):
    issue = Issue.objects.get(pk=pk)
    comments = Comment.objects.filter(issue=issue)
    if request.user.profile == issue.created_by or request.user.is_staff:
        if request.method == "POST":
            body = request.POST.get('comment_body')
            comment = Comment.objects.create(issue=issue, comment=body, user=request.user)
            messages.success(request, "💬 Your Comment has been posted successfully!")
            return redirect('issue_detail', issue.pk)
        return render(request, 'core/issue_detail.html', {'issue': issue, 'comments': comments})
    else:
        return redirect('home')

@login_required
def issue_edit(request, pk):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            messages.success(request, '📩 Your Issue has Edited')
            return redirect('home')
    form = IssueForm()
    return render(request, 'core/report_issue.html', {'form': form})
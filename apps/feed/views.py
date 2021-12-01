from re import I
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from apps.notification.utilities import notify
from apps.feed.utilities import find_mention

from .forms import FeedForm
from .models import Feed, FeedComment


@login_required
def add_feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST, request.FILES)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.created_by = request.user.profile
            feed.save()
            find_mention(request=request, body=feed.body,
                         ntype="FEED", feed=feed)
            messages.success(request, 'Feed added successfully')
            return redirect('home')
    form = FeedForm()
    return render(request, 'feed/feed_form.html', {'form': form})


@login_required
def edit_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    DANGER = 40
    if request.user.profile != feed.created_by:
        messages.add_message(
            request, DANGER, 'You are not allowed to edit this feed')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = FeedForm(request.POST, request.FILES, instance=feed)
            if form.is_valid():
                form.save()
            find_mention(request=request, body=feed.body,
                         ntype="FEED", feed=feed)
            messages.success(request, 'Feed updated successfully')
            return redirect('home')
    form = FeedForm(instance=feed)
    return render(request, 'feed/feed_form.html', {'feed': feed, 'form': form})


def delete_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    DANGER = 40
    if request.user.profile != feed.created_by:
        messages.add_message(
            request, DANGER, 'You are not allowed to delete this feed')
        return redirect('home')
    else:
        if request.method == "POST":
            if request.POST.get('delete') == "Delete":
                feed.delete()
                messages.success(request, 'Feed deleted successfully')
                return redirect('home')
    return render(request, 'feed/feed_delete.html', {'feed': feed})


@login_required
def feed_detail(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    comments = FeedComment.objects.filter(feed=feed)
    return render(request, 'feed/feed_detail.html', {'feed': feed, 'comments': comments})


def add_comment(request):
    if request.method == "POST":
        comment_body = request.POST.get('comment_body')
        feed = get_object_or_404(Feed, id=request.POST.get('feed_id'))
        comment = FeedComment.objects.create(
            body=comment_body, feed=feed, created_by=request.user.profile)
        find_mention(request=request, body=comment_body,
                     ntype="COMMENT", comment=comment, feed=feed)
        messages.success(request, "Comment Added Successfully")
        return redirect('feed_detail', feed.pk)

    else:
        return redirect('home')


@login_required
def like_feed(request):
    if request.method == "POST":
        feed = get_object_or_404(Feed, id=request.POST.get('feed_id'))
        if request.user.profile in feed.likes.all():
            feed.likes.remove(request.user.profile)
            messages.success(request, "Like Removed")
            return redirect('feed_detail', feed.pk)
        elif request.user.profile not in feed.likes.all():
            feed.likes.add(request.user.profile)
            messages.success(request, "Like Successfully")
            notify(message=f"{request.user.username.title} Liked Your Feed",
                   notification_type="like",
                   to_user=feed.created_by, by_user=request.user.profile,
                   link=reverse_lazy('feed_detail', kwargs={'pk': feed.pk}))
            return redirect('feed_detail', feed.pk)
    else:
        return redirect('home')

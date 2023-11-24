from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from django.http import HttpResponse
from apps.feed.forms import CommentForm, FeedForm
from apps.core.utilities import is_htmx_request, paginate
from apps.feed.models import Comment, Plustag, Feed


@login_required
def add_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST, request.FILES)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = request.user
            if request.POST.get("reply_id", None):
                feed.reply_to = feed.objects.get(pk=request.POST.get("reply_id"))
            feed.save()
            messages.success(request, "Feed added successfully")
            return redirect("home")
    form = FeedForm(initial={"body": request.GET.get("feed_body", "")})
    return render(request, "feed/feed_form.html", {"form": form, "title": "Add feed"})


@login_required
def delete_feed(request, pk):
    feed = get_object_or_404(feed, pk=pk, user=request.user)
    if request.method == "POST":
        feed.delete()
        if is_htmx_request(request):
            return HttpResponse("Deleted Successfully")
        messages.success(request, "feed deleted successfully")
        return redirect("home")
    return render(request, "feed/feed_delete.html", {"feed": feed})


def feed_detail(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    if request.user.is_authenticated and request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            return create_comment(form, request, feed, pk)
    form = CommentForm()
    comments = paginate(request, Comment.objects.filter(feed=feed, reply_to__isnull=True))
    return render(
        request,
        "feed/feed_detail.html",
        {
            "feed": feed,
            "form": form,
            "comments": comments,
        },
    )


def create_comment(form, request, feed, pk):
    comment = form.save(commit=False)
    comment.user = request.user
    comment.feed = feed
    if request.POST.get("comment_id"):
        reply_to = get_object_or_404(Comment, pk=request.POST.get("comment_id"))
        comment.reply_to = reply_to
    comment.save()
    if is_htmx_request(request):
        return redirect("_comment_refresh", feed.pk)
    messages.success(request, "Comment added successfully")
    return redirect("feed_detail", pk=pk)


def plustag_feeds(request, p):
    plustag = get_object_or_404(Plustag, name=p)
    feeds = plustag.feed_set.all()
    return render(
        request,
        "feed/plustag_feeds.html",
        {"plustag": plustag, "feeds": paginate(request, feeds)},
    )


def view_comment(request, pk, feed_pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, "feed/comment/view.html", {"comment": comment})


def feed_liked_users(request, feed_pk):
    feed = get_object_or_404(Feed, pk=feed_pk)
    liked_users = paginate(request, feed.likes.all().order_by("-date_joined"))
    return render(request, "feed/feed_liked_users.html", {"liked_users": liked_users})


@login_required
def _comment_form(request):
    comment_id = request.GET.get("comment_id")
    form = CommentForm()
    return render(
        request,
        "feed/islands/comment_form.html",
        {"comment_id": comment_id, "form": form},
    )


def _comment_refresh(request, pk):
    feed = get_object_or_404(feed, pk=pk)
    comments = paginate(request, feed.comment_set.all())
    form = CommentForm()
    return render(
        request,
        "feed/islands/comments.html",
        {"comments": comments, "feed": feed, "form": form},
    )

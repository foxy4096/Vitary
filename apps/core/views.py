from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


from apps.core.forms import ReportForm
from apps.core.models import Badge
from apps.core.templatetags.convert_markdown import convert_markdown
from apps.feed.forms import FeedForm
from apps.feed.models import Feed
from apps.feed.templatetags.mention import user_mention
from apps.core.utilities import paginate


def index(request):
    """
    The Index Page
    """
    return redirect("home")


def frontpage(request):
    """
    The Frontpage
    """
    if request.user.is_authenticated:
        return redirect("feed")

    return render(request, "core/frontpage.html")


@login_required
def feed(request):
    """
    Retun the user feed
    """
    feeds = Feed.objects.filter(
        Q(user=request.user) | 
        Q(user__userprofile__in=request.user.userprofile.follows.all()) | 
        Q(user__userprofile__in=request.user.userprofile.followed_by.all())
    ).order_by("-date") or Feed.objects.all()
    if not request.user.userprofile.allow_nsfw:
        feeds = feeds.exclude(nsfw=True)
    form = FeedForm()
    return render(request, "core/feed.html", {"feeds": paginate(request, feeds), "form": form})


def user_list(request):
    users = paginate(request, User.objects.all().order_by("-userprofile__follower_count"))
    return render(request, "core/user_list.html", {"users": users})


def explore(request):
    feeds = Feed.objects.all().order_by("-like_count", "-date")
    if request.user.is_authenticated and not request.user.userprofile.allow_nsfw:
        feeds = feeds.exclude(nsfw=True)
    context = {
        "feeds": paginate(request, feeds),
    }
    return render(request, "core/explore.html", context)


@login_required
def report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Your report has been submitted successfully")
            return redirect("home")
    else:
        url = request.GET.get("url")
        form = ReportForm(initial={"url": request.build_absolute_uri(url)})
    return render(
        request,
        "core/report_abuse.html",
        {"form": form},
    )


def page_404(request):
    return render(request, "404.html")


def search(request):
    context = {}
    if query := request.GET.get("q", ""):
        feeds = Feed.objects.filter(
            Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(body__icontains=query)
        ).order_by("-date")
        context["feeds"] = paginate(request, feeds)
        context["query"] = query
    return render(request, "core/search.html", context)


@login_required
def convert_markdown_to_html(request):
    input_param = request.POST.get("name", default="value")
    text = request.POST.get(input_param)
    html = convert_markdown(user_mention(text))
    return HttpResponse(html)


@login_required
def intent(request, intent_type, id):
    redirect_url = None

    if intent_type == "like":
        redirect_url = reverse("feed_detail", args=(id,)) + "?like=true"
    elif intent_type == "follow":
        redirect_url = reverse("user_detail", args=(id,)) + "?follow=true"
    else:
        redirect_url = reverse("home")

    return redirect(redirect_url)

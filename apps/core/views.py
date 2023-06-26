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
from apps.core.templatetags import convert_markdown
from apps.vit.forms import VitForm
from apps.vit.models import Vit
from apps.vit.templatetags import mention
from  apps.vit.utilities import paginator_limit





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
    else:
        return render(request, "core/frontpage.html")


@login_required
def feed(request):
    """
    Retun the user feed
    """
    vits = Vit.objects.filter(
        Q(user=request.user)
        | Q(user__profile__in=request.user.profile.follows.all())
        | Q(user__profile__in=request.user.profile.followed_by.all())
    ).order_by("-date")
    if not request.user.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    paginator = (
        Paginator(vits, paginator_limit(request))
        if vits
        else Paginator(Vit.objects.all().order_by("-like_count", "-date"), 10)
    )
    page_no = request.GET.get("page")
    page_obj = paginator.get_page(page_no)
    form = VitForm()
    return render(request, "core/feed.html", {"vits": page_obj, "form": form})


def list_users(request):
    persons = User.objects.all().order_by("-profile__follower_count")
    paginator = Paginator(persons, paginator_limit(request))
    page_no = request.GET.get("page")
    page_obj = paginator.get_page(page_no)
    return render(request, "core/peoples.html", {"persons": page_obj})


def explore(request):
    vits = Vit.objects.all().order_by("-like_count", "-date")
    if request.user.is_authenticated and not request.user.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    paginator = Paginator(vits, paginator_limit(request))
    page_no = request.GET.get("page")
    page_obj = paginator.get_page(page_no)
    context = {
        "vits": page_obj,
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
        vits = Vit.objects.filter(
            Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(body__icontains=query)
        ).order_by("-date")
        paginator = Paginator(vits, paginator_limit(request))
        page_no = request.GET.get("page")
        vits = paginator.get_page(page_no)
        context["vits"] = vits
        context["query"] = query
    return render(request, "core/search.html", context)

def badge(request, pk):
    badge = get_object_or_404(Badge, id=pk)
    usr = badge.profile_set.all().order_by("-id")
    paginator = Paginator(usr, paginator_limit(request))
    page_no = request.GET.get("page")
    page_obj = paginator.get_page(page_no)
    return render(request, "core/badge.html", {"badge": badge, "usrs": page_obj})


def redirect_to_profile(request):
    return redirect("profile")


@login_required
def convert_markdown_to_html(request):
    return HttpResponse(
        convert_markdown.convert_markdown(
            mention.mention(request.POST.get("value", "")), user=request.user
        )
    )


@login_required
def intent(request, intent_type, id):
    redirect_url = None

    if intent_type == "like":
        redirect_url = reverse("vit_detail", args=(id,)) + "?like=true"
    elif intent_type == "follow":
        redirect_url = reverse("user_detail", args=(id,)) + "?follow=true"
    else:
        redirect_url = reverse("home")

    return redirect(redirect_url)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.vit.forms import VitForm
from apps.vit.models import Vit

from apps.core.forms import ReportForm
from apps.core.models import Badge


def index(request):
    return redirect("home")


def frontpage(request):
    if request.user.is_authenticated:
        return redirect("feed")
    else:
        return render(request, "core/frontpage.html")

@login_required
def feed(request):
    vits = Vit.objects.filter(
        Q(user=request.user)
        | Q(user__profile__in=request.user.profile.follows.all())
        | Q(user__profile__in=request.user.profile.followed_by.all())
    ).order_by("-date")
    if not request.user.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    paginator = (Paginator(vits, 10) if vits else Paginator(Vit.objects.all().order_by("-like_count", "-date"), 10))
    page_no = request.GET.get("page")
    page_obj = paginator.get_page(page_no)
    form = VitForm()
    return render(
        request, "core/feed.html", {"vits": page_obj, "form": form}
    )

def peoples(request):
    persons = User.objects.all().order_by("-profile__follower_count")
    paginator = Paginator(persons, 10)
    page_no = request.GET.get("page")
    page_obj = paginator.get_page(page_no)
    return render(request, "core/peoples.html", {"persons": page_obj})


def explore(request):
    vits = Vit.objects.all().order_by("-like_count", "-date")
    if request.user.is_authenticated and not request.user.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    paginator = Paginator(vits, 5)
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
        url = request.GET.get("url", "")
        form = ReportForm(initial={"url": request.build_absolute_uri(url)})
    return render(
        request,
        "core/report_abuse.html",
        {"form": form},
    )


def page_404(request):
    return render(request, "404.html")


def search(request):
    original_query = request.GET.get("q", "")
    query = original_query
    stype = request.GET.get("stype", "")
    if query == "":
        return redirect("home")
    if query[0] == "@" and stype == "":
        stype = "users"
    if query[0] != "@" and stype == "":
        stype = "vits"
    if stype == "vits":
        vits = Vit.objects.filter(
            Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(body__icontains=query)
        ).order_by("-date")
        page_obj = _extracted_from_search_17(vits, request)
        context = {
            "vits": page_obj,
            "stype": "vits",
            "query": query,
        }
        return render(request, "core/search.html", context)
    elif stype == "users":
        query = query.replace("@", "")
        persons = User.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        ).order_by("-date_joined")
        page_obj = _extracted_from_search_17(persons, request)
        return render(
            request,
            "core/search.html",
            {"persons": page_obj, "stype": "users", "query": original_query},
        )
    else:
        return redirect("home")


# TODO Rename this here and in `search`
def _extracted_from_search_17(arg0, request):
    paginator = Paginator(arg0, 5)
    page_no = request.GET.get("page")
    return paginator.get_page(page_no)


def badge(request, pk):
    badge = get_object_or_404(Badge, id=pk)
    usr = badge.profile_set.all().order_by("-id")
    paginator = Paginator(usr, 5)
    page_no = request.GET.get("page")
    page_obj = paginator.get_page(page_no)
    return render(request, "core/badge.html", {"badge": badge, "usrs": page_obj})


def redirect_to_profile(request):
    return redirect("profile")

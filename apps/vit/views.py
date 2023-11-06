from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from django.http import HttpResponse
from apps.vit.forms import CommentForm, VitForm
from .utilities import paginator_limit
from apps.core.utilities import is_htmx_request
from apps.vit.models import Comment, Plustag, Vit


@login_required
def add_vit(request):
    if request.method == "POST":
        form = VitForm(request.POST, request.FILES)
        if form.is_valid():
            vit = form.save(commit=False)
            vit.user = request.user
            if request.POST.get("reply_id", None):
                vit.reply_to = Vit.objects.get(pk=request.POST.get("reply_id"))
            vit.save()
            messages.success(request, "Vit added successfully")
            return redirect("home")
    form = VitForm(initial={"body": request.GET.get("vit_body", "")})
    return render(request, "vit/vit_form.html", {"form": form, "title": "Add Vit"})


@login_required
def edit_vit(request, pk):
    vit = get_object_or_404(Vit, pk=pk, user=request.user)
    if request.method == "POST":
        form = VitForm(request.POST, request.FILES, instance=vit)
        if form.is_valid():
            form.save()
            messages.success(request, "Vit updated successfully")
            return redirect("home")
    form = VitForm(instance=vit)
    return render(
        request,
        "vit/vit_form.html",
        {"vit": vit, "vit_form": form, "title": "Edit Vit"},
    )


@login_required
def delete_vit(request, pk):
    vit = get_object_or_404(Vit, pk=pk, user=request.user)
    if request.method == "POST":
        vit.delete()
        if is_htmx_request(request):
            return HttpResponse("Deleted Successfully")
        messages.success(request, "Vit deleted successfully")
        return redirect("home")
    return render(request, "vit/vit_delete.html", {"vit": vit})


def vit_detail(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    if request.user.is_authenticated and request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            return create_comment(form, request, vit, pk)
    form = CommentForm()
    comments = Comment.objects.filter(vit=vit, reply_to__isnull=True)
    paginator = Paginator(comments, paginator_limit(request))
    page = request.GET.get("page")
    comments = paginator.get_page(page)
    related_persons = [vit.user]
    related_persons.extend(iter(vit.mentions.all()))
    related_persons = list(set(related_persons))
    return render(
        request,
        "vit/vit_detail.html",
        {
            "vit": vit,
            "showView": True,
            "form": form,
            "comments": comments,
            "related_persons": related_persons,
        },
    )


def create_comment(form, request, vit, pk):
    comment = form.save(commit=False)
    comment.user = request.user
    comment.vit = vit
    if request.POST.get("comment_id"):
        reply_to = get_object_or_404(Comment, pk=request.POST.get("comment_id"))
        comment.reply_to = reply_to
    comment.save()
    if is_htmx_request(request):
        return redirect("_comment_refresh", vit.pk)
    messages.success(request, "Comment added successfully")
    return redirect("vit_detail", pk=pk)


def plustag_vits(request, p):
    plustag = get_object_or_404(Plustag, name=p)
    vits = plustag.vit_set.all()
    if request.user.is_authenticated and not request.user.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    paginator = Paginator(vits, paginator_limit(request))
    page = request.GET.get("page")
    vits = paginator.get_page(page)
    return render(request, "vit/plustag_vits.html", {"plustag": plustag, "vits": vits})


def view_comment(request, pk, vit_pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, "vit/comment/view.html", {"comment": comment})


def vit_liked_users(request, vit_pk):
    vit = get_object_or_404(Vit, pk=vit_pk)
    liked_users = vit.likes.all().order_by("-date_joined")
    paginator = Paginator(liked_users, paginator_limit(request))
    page = request.GET.get("page")
    liked_users = paginator.get_page(page)
    return render(request, "vit/vit_liked_users.html", {"liked_users": liked_users})


@login_required
def _comment_form(request):
    comment_id = request.GET.get("comment_id")
    form = CommentForm()
    return render(
        request,
        "vit/islands/comment_form.html",
        {"comment_id": comment_id, "form": form},
    )


def _comment_refresh(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    paginator = Paginator(vit.comment_set.all(), paginator_limit(request))
    page = request.GET.get("page")
    comments = paginator.get_page(page)
    form = CommentForm()
    return render(
        request,
        "vit/islands/comments.html",
        {"comments": comments, "vit": vit, "form": form},
    )

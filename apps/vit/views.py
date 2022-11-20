from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import VitForm, CommentForm
from .models import Comment, Vit, Plustag


@login_required
def add_vit(request):
    if request.method == "POST":
        form = VitForm(request.POST, request.FILES)
        if form.is_valid():
            vit = form.save(commit=False)
            vit.user = request.user
            vit.save()
            messages.success(request, "Vit added successfully")
            return redirect("home")
    form = VitForm(initial={'body': request.GET.get("vit_body", "")})
    print(request.GET.get("vit_body", ""))
    return render(request, "vit/vit_form.html", {"form": form, "title": "Add Vit"})


@login_required
def edit_vit(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    DANGER = 40
    if request.user != vit.user:
        messages.add_message(
            request,
            DANGER,
            "You are not allowed to edit this vit, You can only edit your own vit",
        )
        return redirect("home")
    else:
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
    vit = get_object_or_404(Vit, pk=pk)
    DANGER = 40
    if request.user != vit.user:
        messages.add_message(
            request,
            DANGER,
            "You are not allowed to delete this vit, Just go away from here you filthy animal",
        )
        return redirect("home")
    else:
        if request.method == "POST":
            if request.POST.get("delete") == "Delete":
                vit.delete()
                messages.success(request, "Vit deleted successfully")
                return redirect("home")
    return render(request, "vit/vit_delete.html", {"vit": vit})


def vit_detail(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.vit = vit
                comment.save()
                messages.success(request, "Comment added successfully")
                return redirect("vit_detail", pk=pk)
    form = CommentForm()
    comments = Comment.objects.filter(vit=vit)
    paginator = Paginator(comments, 3)
    page = request.GET.get("page")
    comments = paginator.get_page(page)
    related_persons = [vit.user]
    for user in vit.mentions.all():
        related_persons.append(user)
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


def plustag_vits(request, p):
    plustag = get_object_or_404(Plustag, name=p)
    vits = plustag.vit_set.all()
    if request.user.is_authenticated and not request.user.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    paginator = Paginator(vits, 10)
    page = request.GET.get("page")
    vits = paginator.get_page(page)
    return render(request, "vit/plustag_vits.html", {"plustag": plustag, "vits": vits})


def view_comment(request, pk, vit_pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, "vit/comment/view.html", {"comment": comment})


def vit_liked_users(request, vit_pk):
    vit = get_object_or_404(Vit, pk=vit_pk)
    liked_users = vit.likes.all().order_by('-date_joined')
    paginator = Paginator(liked_users, 10)
    page = request.GET.get("page")
    liked_users = paginator.get_page(page)
    return render(request, "vit/vit_liked_users.html", {"liked_users": liked_users})
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .utilities import notify
from apps.vit.utilities import find_mention, find_plustag

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
            find_mention(request=request, vit=vit)
            find_plustag(vit=vit)
            messages.success(request, "Vit added successfully")
            return redirect("home")
    form = VitForm()
    return render(request, "vit/vit_form.html", {"form": form, "title": "Add Vit"})


@login_required
def edit_vit(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    DANGER = 40
    if request.user != vit.user:
        messages.add_message(request, DANGER, "You are not allowed to edit this vit")
        return redirect("home")
    else:
        if request.method == "POST":
            form = VitForm(request.POST, request.FILES, instance=vit)
            if form.is_valid():
                form.save()
                find_mention(request=request, vit=vit)
                find_plustag(vit=vit)
                messages.success(request, "Vit updated successfully")
                return redirect("home")
    form = VitForm(instance=vit)
    return render(
        request, "vit/vit_form.html", {"vit": vit, "form": form, "title": "Edit Vit"}
    )


def delete_vit(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    DANGER = 40
    if request.user != vit.user:
        messages.add_message(request, DANGER, "You are not allowed to delete this vit")
        return redirect("home")
    else:
        if request.method == "POST":
            if request.POST.get("delete") == "Delete":
                vit.delete()
                messages.success(request, "Vit deleted successfully")
                return redirect("home")
    return render(request, "vit/vit_delete.html", {"vit": vit})


@login_required
def vit_detail(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
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
    return render(
        request, "vit/vit_detail.html", {"vit": vit, "showView": True, "form": form, "comments": comments}
    )

@login_required
def plustag_lists(request):
    plustags = Plustag.objects.all()
    paginator = Paginator(plustags, 10)
    page = request.GET.get('page')
    plustags = paginator.get_page(page)
    return render(request, "vit/plustags.html", {"plustags": plustags})

@login_required
def plustag_vits(request, p):
    plustag = get_object_or_404(Plustag, name=p)
    paginator = Paginator(plustag.vit_set.all(), 10)
    page = request.GET.get('page')
    vits = paginator.get_page(page)
    return render(request, "vit/plustag_vits.html", {"plustag": plustag, "vits": vits})

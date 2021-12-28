from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from .utilities import notify
from apps.vit.utilities import find_mention, find_plustag

from .forms import VitForm
from .models import Vit, Plustag

@login_required
def add_vit(request):
    if request.method == 'POST':
        form = VitForm(request.POST, request.FILES)
        if form.is_valid():
            vit = form.save(commit=False)
            vit.user = request.user
            vit.save()
            if request.POST.get('reply_vit_pk', '') != '':
                reply_vit_pk = request.POST.get('reply_vit_pk', '')
                reply_vit = get_object_or_404(Vit, id=reply_vit_pk)
                vit.to_reply_vits = reply_vit
                reply_vit.save()
                vit.save()
                if reply_vit.user != request.user:
                    notify(message=f"{request.user.username.title()} replied to your Vit - '{reply_vit.body}'", notification_type="reply", to_user=reply_vit.user,
                           by_user=request.user, link=reverse_lazy('vit_detail', kwargs={'pk': vit.id}))
            find_mention(request=request, vit=vit)
            find_plustag(vit=vit)
            messages.success(request, 'Vit added successfully')
            return redirect('home')
    form = VitForm()
    return render(request, 'vit/vit_form.html', {'form': form})


@login_required
def edit_vit(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    DANGER = 40
    if request.user != vit.user:
        messages.add_message(
            request, DANGER, 'You are not allowed to edit this vit')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = VitForm(request.POST, request.FILES, instance=vit)
            if form.is_valid():
                form.save()
                find_mention(request=request, vit=vit)
                find_plustag(vit=vit)
                messages.success(request, 'Vit updated successfully')
                return redirect('home')
    form = VitForm(instance=vit)
    return render(request, 'vit/vit_form.html', {'vit': vit, 'form': form, 'title': 'Edit Vit'})


def delete_vit(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    DANGER = 40
    if request.user != vit.user:
        messages.add_message(
            request, DANGER, 'You are not allowed to delete this vit')
        return redirect('home')
    else:
        if request.method == "POST":
            if request.POST.get('delete') == "Delete":
                vit.delete()
                messages.success(request, 'Vit deleted successfully')
                return redirect('home')
    return render(request, 'vit/vit_delete.html', {'vit': vit})


@login_required
def vit_detail(request, pk):
    vit = get_object_or_404(Vit, pk=pk)
    form = VitForm()
    return render(request, 'vit/vit_detail.html', {'vit': vit, 'showView': True, 'form': form})


def plustag_vits(request, p):
    plustag = get_object_or_404(Plustag, name=p)
    form = VitForm()
    return render(request, 'vit/plustag_vits.html', {'plustag': plustag, 'form': form})

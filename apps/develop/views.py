from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.views.generic import *

import secrets

from .forms import DevProfileCreateForm, DevProfileForm, BotCreationForm, BotEditForm, BotUserForm, WebHookForm
from .models import DevProfile, DocumentationCategory, Documentation, Bot, WebHook
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'develop/home.html')

@login_required
def dashboard(request):
    if not DevProfile.objects.filter(user=request.user).exists():
        messages.success(request, "You don't have a Dev Profile")
        return redirect('develop_join')
    bot_form = BotCreationForm()
    form = DevProfileForm(instance=request.user.devprofile)
    return render(request, 'develop/dashboard.html', {'form': form, 'bot_form': bot_form})

@login_required
def join(request):
    if DevProfile.objects.filter(user=request.user).exists():
        messages.success(request, "You already have a Dev Profile")
        return redirect('develop_dashboard')
    if request.method == "POST":
        form = DevProfileCreateForm(request.POST)
        if form.is_valid():
            devprofile = form.save(commit=False)
            devprofile.user = request.user
            devprofile.save()
            messages.success(request, "Dev Profile Created Successfully!")
            return redirect('develop_dashboard')
        else:
            messages.error(request, "The Form is not valid!")
            return redirect('develop_join')
    form = DevProfileCreateForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email
    })
    return render(request, 'develop/join.html', {'form': form})

class DocsIndexView(ArchiveIndexView):
    model = Documentation
    date_field = 'date'
    context_object_name = 'docs'
    template_name = 'develop/docs/index.html'

class DocsDetailView(DetailView):
    model = Documentation
    context_object_name = 'doc'
    template_name = 'develop/docs/view.html'


@login_required
def bot_create(request):
    if request.method == "POST":
        form = BotCreationForm(request.POST)
        if form.is_valid():
            bot = form.save(commit=False)
            bot.owner = request.user
            bot.private_key = secrets.token_hex(16)
            bot.save()
            messages.success(request, "A Wild Bot appeared!")
            return redirect('develop_bot_detail', id=bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags='danger')
            return redirect('develop_dashboard')
    messages.error(request, "You can't create a bot without a name!", extra_tags='danger')
    return redirect('develop_dashboard')

@login_required
def bot_detail(request, id):
    bot = get_object_or_404(Bot, id=id)
    if bot.owner != request.user:
        messages.error(request, "You can't see this bot!", extra_tags='danger')
        return redirect('develop_dashboard')
    if request.method == "POST":
        bform = BotEditForm(request.POST, instance=bot)
        uform = BotUserForm(request.POST, request.FILES, instance=bot.user.profile)
        if bform.is_valid() and uform.is_valid():
            bot = bform.save()
            uform.save()
            bot.user.profile = uform.save()
            bot.user.first_name = bform.cleaned_data['name']
            bot.user.profile.bio = bform.cleaned_data['description']
            bot.user.profile.save()
            messages.success(request, "Bot Edited Successfully!")
            return redirect('develop_bot_detail', id=bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags='danger')
            return redirect('develop_dashboard')
    bform = BotEditForm(instance=bot)
    uform = BotUserForm(instance=bot.user.profile)
    return render(request, 'develop/bot/detail.html', {'bot': bot, 'bform': bform, 'uform': uform})


@login_required
def bot_delete(request, id):
    bot = get_object_or_404(Bot, id=id)
    if bot.owner != request.user:
        messages.error(request, "You can't delete this bot!", extra_tags='danger')
        return redirect('develop_dashboard')
    else:
        bot.delete()
        messages.success(request, "Bot Deleted Successfully!")
        return redirect('develop_dashboard')

@login_required
def webhook_create(request, id):
    bot = get_object_or_404(Bot, id=id)
    if bot.owner != request.user:
        messages.error(request, "You can't create a webhook for this bot!", extra_tags='danger')
        return redirect('develop_dashboard')
    if request.method == "POST":
        form = WebHookForm(request.POST)
        if form.is_valid():
            webhook = form.save(commit=False)
            webhook.bot = bot
            webhook.save()
            messages.success(request, "A Webhook was created!")
            return redirect('develop_bot_detail', id=bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags='danger')
            return redirect('develop_dashboard')
    form = WebHookForm()
    return render(request, 'develop/bot/webhook_form.html', {'form': form, 'bot': bot})


@login_required
def webhook_delete(request, id, webhook_id):
    webhook = get_object_or_404(WebHook, id=webhook_id)
    if webhook.bot.owner != request.user:
        messages.error(request, "You can't delete this webhook!", extra_tags='danger')
        return redirect('develop_dashboard')
    else:
        webhook.delete()
        messages.success(request, "Webhook Deleted Successfully!")
        return redirect('develop_bot_detail', id=webhook.bot.id)


@login_required
def webhook_edit(request, id, webhook_id):
    webhook = get_object_or_404(WebHook, id=webhook_id)
    if webhook.bot.owner != request.user:
        messages.error(request, "You can't edit this webhook!", extra_tags='danger')
        return redirect('develop_dashboard')
    if request.method == "POST":
        form = WebHookForm(request.POST, instance=webhook)
        if form.is_valid():
            webhook = form.save()
            messages.success(request, "Webhook Edited Successfully!")
            return redirect('develop_bot_detail', id=webhook.bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags='danger')
            return redirect('develop_dashboard')
    form = WebHookForm(instance=webhook)
    return render(request, 'develop/bot/webhook_form.html', {'form': form, 'webhook': webhook})


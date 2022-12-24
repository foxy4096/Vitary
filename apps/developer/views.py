import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.developer.forms import (
    BotCreationForm,
    BotEditForm,
    BotUserForm,
    DevProfileCreateForm,
    DevProfileForm,
    WebHookForm,
)
from apps.developer.models import Bot, DevProfile, Token, WebHook


def home(request):
    return render(request, "developer/home.html")


@login_required
def join(request):
    if DevProfile.objects.filter(user=request.user).exists():
        messages.success(request, "You already have a Dev Profile")
        return redirect("developer_dashboard")
    if request.method == "POST":
        form = DevProfileCreateForm(request.POST)
        if form.is_valid():
            devprofile = form.save(commit=False)
            devprofile.user = request.user
            devprofile.save()
            messages.success(request, "Dev Profile Created Successfully!")
            return redirect("developer_dashboard")
        else:
            messages.error(request, "The Form is not valid!")
            return redirect("developer_join")
    form = DevProfileCreateForm(
        initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }
    )
    return render(request, "developer/join.html", {"form": form})


@login_required
def dashboard(request):
    if not DevProfile.objects.filter(user=request.user).exists():
        messages.success(request, "You don't have a Dev Profile")
        return redirect("developer_join")
    if request.method == "POST":
        form = DevProfileForm(request.POST, instance=request.user.devprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Dev Profile Updated Successfully!")
            return redirect("developer_dashboard")
    else:
        form = DevProfileForm(instance=request.user.devprofile)
        bot_form = BotCreationForm()
        return render(
            request, "developer/dashboard.html", {"form": form, "bot_form": bot_form}
        )


@login_required
def refresh_token(request):
    if not DevProfile.objects.filter(user=request.user).exists():
        messages.success(request, "You don't have a Dev Profile")
        return
    token = Token.objects.get_or_create(devprofile=request.user.devprofile)[0]
    token.refresh_token()
    messages.success(request, "Token Refreshed Successfully!")
    return redirect("developer_dashboard")


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
            return redirect("developer_bot_detail", id=bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags="danger")
            return redirect("developer_dashboard")
    messages.error(
        request, "You can't create a bot without a name!", extra_tags="danger"
    )
    return redirect("developer_dashboard")


@login_required
def bot_detail(request, id):
    bot = get_object_or_404(Bot, id=id)
    if bot.owner != request.user:
        messages.error(request, "You can't see this bot!", extra_tags="danger")
        return redirect("developer_dashboard")
    if request.method == "POST":
        bform = BotEditForm(request.POST, instance=bot)
        uform = BotUserForm(request.POST, request.FILES, instance=bot.user.profile)
        if bform.is_valid() and uform.is_valid():
            bot = bform.save()
            uform.save()
            bot.user.profile = uform.save()
            bot.user.first_name = bform.cleaned_data["name"]
            bot.user.profile.bio = bform.cleaned_data["description"]
            bot.user.profile.save()
            messages.success(request, "Bot Edited Successfully!")
            return redirect("developer_bot_detail", id=bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags="danger")
            return redirect("developer_dashboard")
    bform = BotEditForm(instance=bot)
    uform = BotUserForm(instance=bot.user.profile)
    return render(
        request,
        "developer/bot/detail.html",
        {"bot": bot, "bform": bform, "uform": uform},
    )


@login_required
def bot_delete(request, id):
    bot = get_object_or_404(Bot, id=id, owner=request.user)
    bot.user.delete()
    messages.success(request, "Bot Deleted Successfully!")
    return redirect("developer_dashboard")


@login_required
def webhook_create(request, id):
    bot = get_object_or_404(Bot, id=id, owner=request.user)
    if request.method == "POST":
        form = WebHookForm(request.POST)
        if form.is_valid():
            webhook = form.save(commit=False)
            webhook.bot = bot
            webhook.save()
            messages.success(request, "A Webhook was created!")
            return redirect("developer_bot_detail", id=bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags="danger")
            return redirect("developer_dashboard")
    form = WebHookForm()
    return render(
        request, "developer/bot/webhook_form.html", {"form": form, "bot": bot}
    )


@login_required
def webhook_delete(request, id, webhook_id):
    webhook = get_object_or_404(WebHook, id=webhook_id, bot__owner=request.user)
    webhook.delete()
    messages.success(request, "Webhook Deleted Successfully!")
    return redirect("developer_bot_detail", id=webhook.bot.id)


@login_required
def webhook_edit(request, id, webhook_id):
    webhook = get_object_or_404(WebHook, id=webhook_id, bot_owner=request.user)
    if request.method == "POST":
        form = WebHookForm(request.POST, instance=webhook)
        if form.is_valid():
            webhook = form.save()
            messages.success(request, "Webhook Edited Successfully!")
            return redirect("developer_bot_detail", id=webhook.bot.id)
        else:
            messages.error(request, "The Form is not valid!", extra_tags="danger")
            return redirect("developer_dashboard")
    form = WebHookForm(instance=webhook)
    return render(
        request, "developer/bot/webhook_form.html", {"form": form, "webhook": webhook}
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.develope.models import DevProfile, DocumentationTag, Documentation
from rest_framework.authtoken.models import Token

from .forms import DevProfileCreationForm, DevProfileForm
@login_required
def develope_home(request):
    return render(request, 'develope/develope_home.html')

@login_required
def join_us(request):
    dev_profile = DevProfile.objects.filter(user=request.user)
    if dev_profile.exists():
        messages.add_message(request, 40, 'You already have a Develope profile.', extra_tags='danger')
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = DevProfileCreationForm(request.POST)
            if form.is_valid():
                devprofile = form.save(commit=False)
                devprofile.user = request.user
                Token.objects.get_or_create(user=request.user)[0]
                devprofile.save()
                messages.success(request, 'Your Develope profile has been created!')
                return redirect('dashboard')
        else:
            form = DevProfileCreationForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email})
        return render(request, 'develope/join_us.html', {'form': form})
        


@login_required
def dashboard(request):
    return render(request, 'develope/dashboard.html')

@login_required
def dev_profile(request):
    if request.method == 'POST':
        form = DevProfileForm(request.POST, instance=request.user.devprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Develope profile has been updated!')
            return redirect ('dashboard')
        else:
            messages.add_message(request, 40, 'Please correct the error below.', extra_tags='danger')
            return redirect('dev_profile')
    else:
        form = DevProfileForm(instance=request.user.devprofile)
        return render(request, 'develope/profile.html', {'form': form})


def get_started(request):
    return render(request, 'develope/get_started.html')


def documentation(request):
    tags = DocumentationTag.objects.all()
    return render(request, 'develope/docs/documentation.html', {'tags': tags})

def documentation_tag(request, tag):
    tag = get_object_or_404(DocumentationTag, slug=tag)
    return render(request, 'develope/docs/documentation_tag.html', {'tag': tag})


def documentation_detail(request, tag, title):
    tag = get_object_or_404(DocumentationTag, slug=tag)
    doc = get_object_or_404(Documentation, slug=title)
    return render(request, 'develope/docs/documentation_detail.html', {'tag': tag, 'doc': doc})
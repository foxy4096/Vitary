from django.shortcuts import render, redirect

from django.contrib import messages

from django.views.generic import *


from .forms import DevProfileCreateForm, DevProfileForm
from .models import DevProfile, DocumentationCategory, Documentation
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'develop/home.html')

@login_required
def dashboard(request):
    if not DevProfile.objects.filter(user=request.user).exists():
        messages.success(request, "You don't have a Dev Profile")
        return redirect('develop_join')

    if request.method == "POST":
        form = DevProfileForm(request.POST, instance=request.user.devprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated")
            return redirect('develop_dashboard')
    form = DevProfileForm(instance=request.user.devprofile)
    return render(request, 'develop/dashboard.html', {'form': form})

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

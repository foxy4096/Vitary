from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from apps.vit.forms import VitForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DonationProofForm, ReportAbuseForm, DonationProof, BadgeRequestForm

from django.conf import settings
import stripe
from django.core.mail import mail_managers

from apps.vit.models import Vit
from django.contrib.auth.models import User
from .models import Badge, Donation


def redirect_to_home(request):
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        vits = Vit.objects.filter(Q(user=request.user) | Q(
            user__profile__in=request.user.profile.follows.all()) | Q(user__profile__in=request.user.profile.followed_by.all())).order_by('-date')
        paginator = Paginator(vits, 5)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)
        form = VitForm()
        return render(request, 'core/home/home_logged_in.html', {'vits': page_obj, 'form': form})
    else:
        return render(request, 'core/home/home_logged_out.html', {'show': False})


def peoples(request):
    persons = User.objects.all().order_by('-date_joined')
    paginator = Paginator(persons, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, 'core/peoples.html', {'persons': page_obj})

def explore(request):
    vits = Vit.objects.all().order_by('-like_count', '-date')
    paginator = Paginator(vits, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    context = {
        'vits': page_obj,
    }
    return render(request, 'core/explore.html', context)


@login_required
def report_abuse(request, pk):
    if request.method == 'POST':
        form = ReportAbuseForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.to_vit = get_object_or_404(Vit, id=pk)
            report.user = request.user
            report.save()
            messages.success(request, 'Your report has been submitted successfully')
            return redirect('home')
    else:
        form = ReportAbuseForm()
    return render(request, 'core/report_abuse.html', {'form': form, 'vit': get_object_or_404(Vit, id=pk)})


def page_404(request):
    return render(request, '404.html')

def search(request):
    original_query = request.GET.get('q', '')
    query = original_query
    stype = request.GET.get('stype', '')
    if query != '':
        if query[0] == '@' and stype == '':
            stype = 'users'
        if query[0] != '@' and stype == '':
            stype = 'vits'
        if stype == 'vits':
            vits = Vit.objects.filter(Q(user__username__icontains=query) | Q(
                user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(
                body__icontains=query)).order_by('-date')
            paginator = Paginator(vits, 5)
            page_no = request.GET.get('page')
            page_obj = paginator.get_page(page_no)
            context = {
                'vits': page_obj,
                'stype': 'vits',
                'query': query,
            }
            return render(request, 'core/search.html', context)
        elif stype == 'users':
            query = query.replace('@', '')
            persons = User.objects.filter(Q(username__icontains=query) | Q(
                first_name__icontains=query) | Q(last_name__icontains=query)).order_by('-date_joined')
            paginator = Paginator(persons, 5)
            page_no = request.GET.get('page')
            page_obj = paginator.get_page(page_no)
            return render(request, 'core/search.html', {'persons': page_obj, 'stype': 'users', 'query': original_query})
        else:
            return redirect('home')
    else:
        return redirect('home')



def badge(request, pk):
    badge = get_object_or_404(Badge, id=pk)
    usr = badge.profile_set.all().order_by('-id')
    paginator = Paginator(usr, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, 'core/badge.html', {'badge': badge, 'usrs': page_obj})


@login_required
def donate(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    proof_form = DonationProofForm()
    if request.method == "POST":
        if request.POST.get('DTYPE') == 'STRIPT':
            stripe.api_key = settings.STRIPE_SECRET_KEY
            amount = int(request.POST['amount'])
            token = request.POST['stripeToken']
            try:
                charge = stripe.Charge.create(
                    amount=amount * 100,
                    currency='inr',
                    description='Donation to Vitary',
                    source=token,
                )
                Donation.objects.create(
                    user=request.user,
                    amount=amount,
                    stripe_charge_id=charge['id']
                )
                badge = Badge.objects.get_or_create(
                        name="Donator 💸",
                        description="This badge is given to people who have donated to us, to keep our server running and helped Vitary to stay alive",
                        color="warning",
                        special=True
                )[0]
                request.user.profile.badges.set([badge])
                return render(request, 'core/donate_success.html')
            except stripe.error.CardError as e:
                messages.error(request, 'Your card was declined!')
                print(e)
                return redirect('donate')
        elif request.POST.get('DTYPE') == 'OTHER':
            proof_form = DonationProofForm(request.POST, request.FILES)
            if proof_form.is_valid():
                proof = proof_form.save(commit=False)
                proof.user = request.user
                proof.save()
                mail_managers(
                    'Donation Proof Submitted',
                    'A user has submitted a donation proof. Please check the admin panel for more details.'
                )
                messages.success(request, 'Your proof has been submitted successfully')
                return render(request, 'core/donate_success_other.html')
    return render(request, 'core/donate.html', {'stripe_public_key': stripe_public_key, 'proof_form': proof_form})


def all_donations(request):
    donations = Donation.objects.all().order_by('-date')
    paginator = Paginator(donations, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, 'core/all_donations.html', {'donations': page_obj})


@login_required
def my_donations(request):
    donations = Donation.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(donations, 5)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, 'core/my_donations.html', {'donations': page_obj})

@login_required
def request_badge(request, pk):
    badge = get_object_or_404(Badge, id=pk)
    if badge in request.user.profile.badges.all():
        messages.error(request, 'You already have this badge!')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = BadgeRequestForm(request.POST)
            if form.is_valid():
                request_badge = form.save(commit=False)
                request_badge.badge = badge
                request_badge.user = request.user
                request_badge.save()
                mail_managers(
                    subject='Badge Request',
                    message='A user has requested a badge.\n\nBadge: ' + badge.name + '\n\nUser: ' + request.user.username + '\n\nMessage: ' + request_badge.message,
                    fail_silently=True
                )
                messages.success(request, 'Your request has been submitted successfully')
                return redirect('home')
        else:
            form = BadgeRequestForm()
        return render(request, 'core/request_badge.html', {'form': form, 'badge': badge})


def redirect_to_profile(request):
    return redirect('profile')
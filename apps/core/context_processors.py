from .models import Donation

def latest_donations(request):
        donations = Donation.objects.all().order_by('-date')[:5]
        return {'latest_donations': donations}
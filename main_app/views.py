from django.shortcuts import render
from .models import Campaign

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def campaigns_index(request):
  campaigns = Campaign.objects.all()
  return render(request, 'campaigns/index.html', {
    'campaigns': campaigns
  })

def campaigns_details(request, campaign_id):
  campaign = Campaign.objects.get(id=campaign_id)
  return render(request, 'campaigns/detail.html', {
    'campaign': campaign
  })
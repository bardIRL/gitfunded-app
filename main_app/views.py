from django.shortcuts import render
from django.views.generic.edit import DeleteView
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

def campaigns_detail(request, campaign_id):
  campaign = Campaign.objects.get(id=campaign_id)
  return render(request, 'campaigns/detail.html', {
    'campaign': campaign
  })

class CampaignDelete(DeleteView):
  model = Campaign
  success_url = '/campaigns'
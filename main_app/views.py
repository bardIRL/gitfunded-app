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
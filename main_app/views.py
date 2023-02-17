import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Sum
from .models import Campaign, Donation, Photo, CATEGORIES
from .forms import DonationForm

# Custom mixins.
class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        campaign = self.get_object()
        return campaign.user == self.request.user
    def handle_no_permission(self):
        campaign_id = self.kwargs['pk']
        return redirect('detail', campaign_id=campaign_id)
    
# Create your views here.
def home(request):
  campaigns = Campaign.objects.all()
  donations = Donation.objects.all()
  number_of_campaigns = campaigns.count()
  number_of_donations = donations.count()
  recent_campaigns = Campaign.objects.order_by('-id')[:8]

  return render(request, 'home.html', {
    'campaigns': campaigns,
    'number_of_campaigns': number_of_campaigns,
    'number_of_donations': number_of_donations,
    'recent_campaigns': recent_campaigns,
  })

def about(request):
  return render(request, 'about.html')

def campaigns_index(request):
  campaigns = Campaign.objects.all().order_by('-id')
  categories = CATEGORIES
  category = request.GET.get('category')
  if category:
    campaigns = Campaign.objects.filter(category=category).order_by('-id')
  else:
    campaigns = Campaign.objects.all().order_by('-id')

  return render(request, 'campaigns/index.html', {
    'campaigns': campaigns,
    'categories': categories,
    'selected_category': category,
  })

@login_required
def user_campaigns_index(request, user_id):
   campaigns = Campaign.objects.filter(user_id=user_id).order_by('-id')
   return render(request, 'campaigns/user_campaigns.html', {
      'campaigns': campaigns
  })

def campaigns_detail(request, campaign_id):
  campaign = Campaign.objects.get(id=campaign_id)
  donations = Donation.objects.filter(campaign=campaign).order_by('-id')
  number_of_donations = donations.count()
  total_donations = donations.aggregate(Sum('amount'))['amount__sum'] or 0
  if total_donations is not None:
      goal_percentage = min(int(total_donations / campaign.goal * 100), 100)
  else:
      goal_percentage = 0
  donation_form = DonationForm()
  return render(request, 'campaigns/detail.html', {
    'campaign': campaign, 
    'donations': donations, 
    'total_donations': total_donations,
    'goal_percentage': goal_percentage, 
    'number_of_donations': number_of_donations, 
    'donation_form': donation_form
  })

class CampaignCreate(LoginRequiredMixin, CreateView):
  model = Campaign
  fields = ['title', 'category', 'goal', 'link', 'about']
  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)

class CampaignDelete(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
  model = Campaign
  success_url = '/campaigns'

class CampaignUpdate(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
  model = Campaign
  fields = ['title', 'category', 'goal', 'link', 'about']
  success_url = ''

@login_required
def add_donation(request, campaign_id):
  form = DonationForm(request.POST)
  if form.is_valid():
    new_donation = form.save(commit=False)
    new_donation.campaign_id = campaign_id
    new_donation.save()
  return redirect('detail', campaign_id=campaign_id)

@login_required
def add_photo(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    photo_file = request.FILES.get('photo-file', None)
    if request.user != campaign.user:
        messages.error(request, f"You are not authorized to add photos to this campaign.")
        return redirect('detail', campaign_id=campaign_id)
    max_photos = 1 
    if campaign.photo_set.count() >= max_photos:
        messages.error(request, f"You can only upload {max_photos} photo for this campaign.")
        return redirect('detail', campaign_id=campaign_id)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, campaign_id=campaign_id)
            messages.success(request, f"Successfully uploaded!")
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', campaign_id=campaign_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
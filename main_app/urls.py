from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('campaigns/', views.campaigns_index, name='index'),
  path('campaigns/<int:campaign_id>/', views.campaigns_detail, name='detail'),
  path('campaigns/create/', views.CampaignCreate.as_view(), name='campaigns_create'),
  path('campaigns/<int:pk>/delete/', views.CampaignDelete.as_view(), name='campaigns_delete'),
  path('campaigns/<int:pk>/update/', views.CampaignUpdate.as_view(), name='campaigns_update'),
  path('campaigns/<int:campaign_id>/add_photo', views.add_photo, name='add_photo'),
]
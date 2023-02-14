from django.contrib import admin
from .models import Campaign, Donation, Photo

# Register your models here.
admin.site.register(Campaign)
admin.site.register(Donation)
admin.site.register(Photo)
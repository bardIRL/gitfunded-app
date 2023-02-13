from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Campaign(models.Model):
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=100)
    goal = models.IntegerField()
    goal_date = models.DateField()
    about = models.TextField(max_length=1000)
    links = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Donation(models.Model):
    amount = models.IntegerField()
    message = models.TextField(max_length=300)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
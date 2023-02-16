# Generated by Django 4.1.6 on 2023-02-16 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_remove_donation_user_donation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='about',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='category',
            field=models.CharField(choices=[('animals', 'Animals'), ('business', 'Business'), ('community', 'Community'), ('competition', 'Competition'), ('creative', 'Creative'), ('education', 'Education'), ('environment', 'Environment'), ('event', 'Event'), ('faith', 'Faith'), ('family', 'Family'), ('financial-emergency', 'Financial Emergency'), ('medical', 'Medical'), ('memorial', 'Memorial'), ('nonprofit', 'Nonprofit'), ('sports', 'Sports'), ('travel', 'Travel'), ('volunteer', 'Volunteer'), ('wishes', 'Wishes')], max_length=100),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]

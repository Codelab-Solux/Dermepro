# Generated by Django 4.2 on 2024-04-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_profile_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='job_position',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]

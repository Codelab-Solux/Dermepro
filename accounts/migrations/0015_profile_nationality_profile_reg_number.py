# Generated by Django 4.2 on 2024-02-19 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_userstatus_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nationality',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='reg_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
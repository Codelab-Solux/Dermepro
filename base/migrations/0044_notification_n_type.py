# Generated by Django 4.2 on 2024-04-08 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_appointment_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='n_type',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]

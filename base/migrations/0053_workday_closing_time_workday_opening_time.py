# Generated by Django 4.2 on 2024-04-20 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_rename_accepted_at_visit_started_at_visit_ended_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='workday',
            name='closing_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workday',
            name='opening_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
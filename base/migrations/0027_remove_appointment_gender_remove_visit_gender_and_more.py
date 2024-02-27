# Generated by Django 4.2 on 2024-02-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='gender',
        ),
        migrations.AddField(
            model_name='appointment',
            name='sex',
            field=models.CharField(blank=True, choices=[('female', 'Feminin'), ('male', 'Masculin')], default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='sex',
            field=models.CharField(blank=True, choices=[('female', 'Feminin'), ('male', 'Masculin')], default='', max_length=50, null=True),
        ),
    ]

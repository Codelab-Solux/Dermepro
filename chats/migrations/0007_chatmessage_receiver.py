# Generated by Django 4.1.9 on 2023-06-11 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0006_chatnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='receiver',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
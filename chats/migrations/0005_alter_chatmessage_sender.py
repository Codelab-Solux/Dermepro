# Generated by Django 4.1.9 on 2023-06-09 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_chatmessage_alter_thread_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='sender',
            field=models.IntegerField(default=None),
        ),
    ]
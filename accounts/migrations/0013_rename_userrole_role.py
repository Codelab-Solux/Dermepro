# Generated by Django 4.2 on 2023-05-18 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_customuser_role'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserRole',
            new_name='Role',
        ),
    ]

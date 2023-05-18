# Generated by Django 4.1.7 on 2023-04-12 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('fr_name', models.CharField(
                    max_length=255, default='', null=True, blank=True)),
                ('sec_level', models.IntegerField(
                    db_index=True, max_length=255, unique=True)),
            ],
        ),
    ]
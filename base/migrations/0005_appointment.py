# Generated by Django 4.1.7 on 2023-04-03 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_delete_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest', models.CharField(max_length=255)),
                ('tel', models.CharField(default='', max_length=128)),
                ('nationality', models.CharField(default='', max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('arrived_at', models.DateTimeField(blank=True, null=True)),
                ('departed_at', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Masculin'), ('female', 'Feminin')], default='', max_length=50, null=True)),
                ('id_doc', models.CharField(blank=True, choices=[('id_card', "Carte d'identité"), ('vote_card', "Carte d'électeur"), ('drv_license', 'Permit de conduire'), ('passport', 'Passport international')], default='', max_length=50, null=True)),
                ('status', models.CharField(blank=True, choices=[('pending', 'En attente'), ('open', 'En cours'), ('closed', 'Cloturée'), ('ajourned', 'Ajournée'), ('cancelled', 'Annulée')], default='pending', max_length=50, null=True)),
                ('signature', models.CharField(default='', max_length=255)),
                ('is_vip', models.BooleanField(default='False')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
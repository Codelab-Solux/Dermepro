# Generated by Django 4.1.7 on 2023-04-03 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_alter_appointment_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='arrived_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='departed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='is_vip',
            field=models.BooleanField(default='False'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='nationality',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='appointment',
            name='signature',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='id_doc',
            field=models.CharField(blank=True, choices=[('id_card', "Carte d'identité"), ('vote_card', "Carte d'électeur"), ('drv_license', 'Permit de conduire'), ('passport', 'Passport international')], default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'En attente'), ('open', 'En cours'), ('closed', 'Cloturée'), ('ajourned', 'Ajournée'), ('cancelled', 'Annulée')], default='pending', max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Visit',
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
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

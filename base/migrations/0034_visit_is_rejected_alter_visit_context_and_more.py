# Generated by Django 4.2 on 2024-03-07 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_alter_appointment_phone_alter_appointment_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='visit',
            name='context',
            field=models.CharField(choices=[('friendly', 'Amicale'), ('familial', 'Familiale'), ('professional', 'Professionelle')], max_length=50),
        ),
        migrations.AlterField(
            model_name='visit',
            name='id_document',
            field=models.CharField(choices=[('id_card', "Carte Nationale d'Identité (CNI)"), ('consul_card', 'Carte Consulaire'), ('ecowas_card', 'Carte CEDEAO'), ('driver_license', 'Permit de conduire'), ('passport', 'Passport international')], max_length=50),
        ),
    ]
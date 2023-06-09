# Generated by Django 4.1.7 on 2023-04-25 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_appointment_civility_visit_civility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='civility',
            field=models.CharField(blank=True, choices=[('M.', 'M.'), ('Mme.', 'Mme.'), ('Mlle.', 'Mlle.')], default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='civility',
            field=models.CharField(blank=True, choices=[('M.', 'M.'), ('Mme.', 'Mme.'), ('Mlle.', 'Mlle.')], default='', max_length=50, null=True),
        ),
    ]

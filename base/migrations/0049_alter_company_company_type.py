# Generated by Django 4.2 on 2024-04-13 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_alter_company_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_type',
            field=models.CharField(choices=[('SC', 'SC'), ('SA', 'SA'), ('SAS', 'SAS'), ('SNS', 'SNS'), ('SNC', 'SNC'), ('SANC', 'SANC'), ('SARL', 'SARL'), ('SARLU', 'SARLU')], max_length=50),
        ),
    ]

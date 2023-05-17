# Generated by Django 4.1.7 on 2023-05-02 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_appointment_civility_alter_visit_civility'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='context',
            field=models.CharField(blank=True, choices=[('amicale', 'Amicale'), ('familial', 'Familiale'), ('professionelle', 'Professionelle')], default='professionelle', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='civility',
            field=models.CharField(blank=True, choices=[('M.', 'Monsieur'), ('Mme.', 'Madame'), ('Mlle.', 'Mademoiselle')], default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='civility',
            field=models.CharField(blank=True, choices=[('M.', 'Monsieur'), ('Mme.', 'Madame'), ('Mlle.', 'Mademoiselle')], default='', max_length=50, null=True),
        ),
    ]

# Generated by Django 4.2 on 2024-04-16 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0049_alter_company_company_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='n_type',
            new_name='notice',
        ),
        migrations.AddField(
            model_name='appointment',
            name='context',
            field=models.CharField(choices=[('friendly', 'Amicale'), ('familial', 'Familiale'), ('professional', 'Professionelle')], default='professional', max_length=50),
        ),
    ]
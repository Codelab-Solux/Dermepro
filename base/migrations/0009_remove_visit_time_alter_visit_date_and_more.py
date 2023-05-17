# Generated by Django 4.1.7 on 2023-04-11 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_appointment_is_vip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='time',
        ),
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='nationality',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='tel',
            field=models.CharField(blank=True, default='', max_length=128, null=True),
        ),
    ]

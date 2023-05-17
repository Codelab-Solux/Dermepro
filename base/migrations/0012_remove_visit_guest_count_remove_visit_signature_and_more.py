# Generated by Django 4.1.7 on 2023-04-23 18:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_visit_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='guest_count',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='signature',
        ),
        migrations.AddField(
            model_name='visit',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='visit',
            name='arrived_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='doc_num',
            field=models.IntegerField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='tel',
            field=models.IntegerField(blank=True, default='', max_length=128, null=True),
        ),
    ]

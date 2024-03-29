# Generated by Django 4.2 on 2024-02-09 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_chatnotification_delete_visit_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='visit',
            name='accepted_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='arrived_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='departed_at',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

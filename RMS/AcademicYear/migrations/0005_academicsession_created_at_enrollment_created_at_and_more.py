# Generated by Django 4.2 on 2024-08-17 16:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AcademicYear', '0004_alter_academicsession_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicsession',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='semester',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='staffassignment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

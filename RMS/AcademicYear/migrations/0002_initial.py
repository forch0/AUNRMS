# Generated by Django 4.2 on 2024-07-13 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AcademicYear', '0001_initial'),
        ('Dorms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffassignment',
            name='dorm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dorms.dorm'),
        ),
    ]

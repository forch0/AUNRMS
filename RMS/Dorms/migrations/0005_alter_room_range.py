# Generated by Django 4.2 on 2024-08-01 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dorms', '0004_room_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='range',
            field=models.CharField(blank=True, choices=[('101-116', '101-116'), ('201-216', '201-216'), ('301-316', '301-316')], max_length=20, null=True),
        ),
    ]

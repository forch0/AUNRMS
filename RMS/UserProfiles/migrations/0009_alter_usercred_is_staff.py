# Generated by Django 4.2 on 2024-09-20 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfiles', '0008_alter_residents_options_alter_staffs_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercred',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.2 on 2024-08-16 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfiles', '0002_residents_guardianphonenumber_usercred_phonenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='residents',
            name='room',
        ),
    ]

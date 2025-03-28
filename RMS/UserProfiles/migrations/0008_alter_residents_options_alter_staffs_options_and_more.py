# Generated by Django 4.2 on 2024-09-18 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfiles', '0007_alter_usercred_email_alter_usercred_is_superuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='residents',
            options={'ordering': ['user__email'], 'verbose_name': 'resident', 'verbose_name_plural': 'residents'},
        ),
        migrations.AlterModelOptions(
            name='staffs',
            options={'ordering': ['user__email'], 'verbose_name': 'staff', 'verbose_name_plural': 'staffs'},
        ),
        migrations.AlterModelOptions(
            name='usercred',
            options={'ordering': ['email'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='usercred',
            name='username',
        ),
    ]

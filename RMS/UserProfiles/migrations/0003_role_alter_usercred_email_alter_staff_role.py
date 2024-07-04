# Generated by Django 4.2 on 2024-07-04 14:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfiles', '0002_alter_usercred_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='usercred',
            name='email',
            field=models.EmailField(blank=True, default='aun@example.com', max_length=255, validators=[django.core.validators.RegexValidator(message='Email must be from aun.edu.ng domain.', regex='@aun\\.edu\\.ng$')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staff',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserProfiles.role'),
        ),
    ]

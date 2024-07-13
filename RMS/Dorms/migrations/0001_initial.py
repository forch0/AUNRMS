# Generated by Django 4.2 on 2024-07-05 13:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dorms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('campus_status', models.CharField(choices=[('ON', 'On Campus'), ('OFF', 'Off Campus')], default='ON', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('number', models.CharField(max_length=20)),
                ('capacity', models.IntegerField()),
                ('floor', models.IntegerField()),
                ('dorm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='Dorms.dorms')),
            ],
        ),
        migrations.CreateModel(
            name='Storages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('description', models.TextField()),
                ('capacity', models.IntegerField()),
                ('current_capacity', models.IntegerField(default=0)),
                ('dorm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storages', to='Dorms.dorms')),
            ],
        ),
        migrations.CreateModel(
            name='StorageItems',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Dorms.rooms')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Dorms.storages')),
            ],
        ),
    ]

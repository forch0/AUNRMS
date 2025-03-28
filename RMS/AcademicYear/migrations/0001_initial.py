# Generated by Django 4.2 on 2024-07-13 15:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('name', models.CharField(blank=True, editable=False, help_text='Automatically formatted as start_year/end_year', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_enrolled', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('semester_type', models.CharField(choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')], max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='StaffAssignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AcademicYear.academicsession')),
            ],
            options={
                'verbose_name': 'Staff Assignment',
                'verbose_name_plural': 'Staff Assignments',
            },
        ),
    ]

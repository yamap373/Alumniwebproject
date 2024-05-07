# Generated by Django 5.0.2 on 2024-04-11 10:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_Alumni_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Undefined')], max_length=1)),
                ('dob', models.DateField(blank=True, null=True)),
                ('started_year', models.DateField()),
                ('graduated_year', models.DateField()),
                ('bio', models.TextField(blank=True)),
                ('grad_high_school', models.CharField(blank=True, max_length=100)),
                ('internship_position', models.CharField(blank=True, max_length=100)),
                ('show_contact_info', models.BooleanField(default=False)),
                ('line', models.CharField(blank=True, max_length=100)),
                ('facebook', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('internship_workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_internship_workplaces', to='MIS_Alumni_App.workplace')),
            ],
        ),
        migrations.CreateModel(
            name='AlumniProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alumni_email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('student_id', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Undefined')], max_length=1)),
                ('dob', models.DateField(blank=True, null=True)),
                ('started_year', models.DateField()),
                ('graduated_year', models.DateField()),
                ('bio', models.TextField(blank=True)),
                ('current_position', models.CharField(blank=True, max_length=100)),
                ('previous_position', models.CharField(blank=True, max_length=100)),
                ('show_contact_info', models.BooleanField(default=False)),
                ('line', models.CharField(blank=True, max_length=100)),
                ('facebook', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alumni_current_workplaces', to='MIS_Alumni_App.workplace')),
                ('previous_workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alumni_previous_workplaces', to='MIS_Alumni_App.workplace')),
            ],
        ),
    ]
# Generated by Django 5.0.2 on 2024-04-19 08:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_Alumni_App', '0010_event_news_alter_studentprofile_student_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumniprofile',
            name='alumni_email',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='current_position',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='current_workplace',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='line',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='previous_position',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='previous_workplace',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='show_contact_info',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='alumniprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='alumniprofile',
            name='mentor_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alumni_email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_alumni', models.BooleanField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Undefined')], max_length=1, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('show_contact_info', models.BooleanField(default=False)),
                ('line', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='alumniPF/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentStudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentee_status', models.BooleanField(default=False, null=True)),
                ('started_year', models.IntegerField(blank=True, null=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='MIS_Alumni_App.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='alumniprofile',
            name='user_profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='MIS_Alumni_App.userprofile'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='StudentProfile',
        ),
    ]

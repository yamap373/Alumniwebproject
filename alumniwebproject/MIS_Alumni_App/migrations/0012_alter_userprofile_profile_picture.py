# Generated by Django 5.0.2 on 2024-04-19 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_Alumni_App', '0011_remove_alumniprofile_alumni_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='ProfileUserPF/'),
        ),
    ]
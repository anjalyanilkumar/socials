# Generated by Django 4.1.2 on 2023-03-16 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0014_alter_profile_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followers',
        ),
    ]

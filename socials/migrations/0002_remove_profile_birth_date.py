# Generated by Django 4.1.2 on 2023-01-01 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
    ]

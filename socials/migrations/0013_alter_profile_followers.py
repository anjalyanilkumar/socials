# Generated by Django 4.1.2 on 2023-03-16 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0012_alter_profile_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='followers', to='socials.profile'),
        ),
    ]
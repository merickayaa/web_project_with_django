# Generated by Django 4.2.1 on 2023-12-12 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_followers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
    ]

# Generated by Django 4.2.1 on 2023-12-08 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_likepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='username_of_likes',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

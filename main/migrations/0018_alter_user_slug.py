# Generated by Django 4.2.1 on 2023-12-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
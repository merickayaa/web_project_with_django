# Generated by Django 4.2.1 on 2023-12-10 13:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, unique=True),
        ),
    ]
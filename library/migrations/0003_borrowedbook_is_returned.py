# Generated by Django 4.2.9 on 2024-02-14 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowedbook',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]

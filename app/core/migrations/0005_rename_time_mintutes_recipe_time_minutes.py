# Generated by Django 3.2.25 on 2024-05-12 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time_mintutes',
            new_name='time_minutes',
        ),
    ]

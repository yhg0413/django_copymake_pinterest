# Generated by Django 4.1 on 2022-09-06 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articleapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='context',
            new_name='content',
        ),
    ]

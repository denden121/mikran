# Generated by Django 3.0.7 on 2020-06-18 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0008_auto_20200618_0232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='second_name',
            new_name='last_name',
        ),
    ]

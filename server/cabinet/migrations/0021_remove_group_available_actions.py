# Generated by Django 3.0 on 2020-09-15 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0020_profile_employment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='available_actions',
        ),
    ]

# Generated by Django 3.0 on 2020-07-09 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='action_num',
        ),
    ]
# Generated by Django 3.0 on 2020-08-19 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0010_auto_20200819_0337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subdepartment',
            old_name='subdepartment',
            new_name='subdepartment_code',
        ),
    ]

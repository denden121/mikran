# Generated by Django 3.0 on 2020-08-19 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0008_auto_20200818_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarmark',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cabinet.Profile'),
        ),
    ]

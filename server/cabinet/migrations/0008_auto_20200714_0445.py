# Generated by Django 3.0 on 2020-07-14 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0007_auto_20200714_0423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
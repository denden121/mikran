# Generated by Django 3.0 on 2020-10-05 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0031_auto_20201005_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]

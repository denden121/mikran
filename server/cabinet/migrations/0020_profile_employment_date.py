# Generated by Django 3.0 on 2020-09-15 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0019_profile_oklad'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='employment_date',
            field=models.DateField(blank=True, default='2010-01-01', null=True),
        ),
    ]
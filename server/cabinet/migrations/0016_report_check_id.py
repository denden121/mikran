# Generated by Django 3.0 on 2020-09-10 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0015_auto_20200910_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='check_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checker', to='cabinet.Profile'),
        ),
    ]
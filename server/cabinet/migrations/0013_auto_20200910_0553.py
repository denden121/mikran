# Generated by Django 3.0 on 2020-09-10 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0012_auto_20200908_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='ban_id',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ban', to='cabinet.Profile'),
        ),
        migrations.AlterField(
            model_name='report',
            name='creator_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to='cabinet.Profile'),
        ),
    ]
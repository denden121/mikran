# Generated by Django 3.0 on 2020-07-15 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0011_auto_20200715_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='project',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_id', to='cabinet.Project'),
        ),
    ]

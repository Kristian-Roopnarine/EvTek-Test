# Generated by Django 3.0.8 on 2020-07-20 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_bins', '0002_auto_20200720_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pickup',
            name='scheduled_time',
        ),
        migrations.AlterField(
            model_name='pickup',
            name='scheduled_date',
            field=models.DateTimeField(),
        ),
    ]

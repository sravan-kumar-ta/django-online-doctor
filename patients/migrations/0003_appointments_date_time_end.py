# Generated by Django 4.0.6 on 2022-10-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_remove_appointments_date_time_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='date_time_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.2.3 on 2025-06-30 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='appointment',
            index=models.Index(fields=['provider', 'start_time'], name='scheduler_a_provide_f4ee24_idx'),
        ),
    ]

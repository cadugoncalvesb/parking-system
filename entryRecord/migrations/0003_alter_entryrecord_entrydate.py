# Generated by Django 5.2.2 on 2025-06-13 16:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entryRecord', '0002_alter_entryrecord_entrydate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryrecord',
            name='entryDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

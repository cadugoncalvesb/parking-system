# Generated by Django 5.2.2 on 2025-06-09 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='totalVacancies',
            field=models.IntegerField(),
        ),
    ]

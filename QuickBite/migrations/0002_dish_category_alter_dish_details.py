# Generated by Django 5.1.3 on 2024-11-15 23:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuickBite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QuickBite.category'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='details',
            field=models.TextField(blank=True),
        ),
    ]

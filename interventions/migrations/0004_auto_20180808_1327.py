# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-08 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interventions', '0003_auto_20180808_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='session_frequency',
            field=models.TextField(blank=True, verbose_name='Wat is de frequentie van de interventie?'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='amount_per_week',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Hoe vaak per week vindt de interventiesessie plaats?'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='version',
            field=models.PositiveIntegerField(default=2, verbose_name='INTERNAL - Describes which version of the intervention model is used'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-29 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_setting_is_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='is_school',
            field=models.BooleanField(default=False, verbose_name='Needs external permission'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20160419_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationkind',
            name='registration',
        ),
        migrations.AlterField(
            model_name='task',
            name='registration_kinds',
            field=models.ManyToManyField(to='core.RegistrationKind', verbose_name='Kies het soort meting', blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='registrations',
            field=models.ManyToManyField(to='core.Registration', verbose_name='Hoe wordt het gedrag of de toestand van de deelnemer bij deze taak vastgelegd?'),
        ),
        migrations.DeleteModel(
            name='Registration',
        ),
        migrations.DeleteModel(
            name='RegistrationKind',
        ),
    ]

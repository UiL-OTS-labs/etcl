# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_registration_registrationkind'),
        ('interventions', '0007_auto_20160503_1235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intervention',
            old_name='has_controls_details',
            new_name='controls_description',
        ),
        migrations.RenameField(
            model_name='intervention',
            old_name='has_recording',
            new_name='has_prepost',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='number',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='recording_experimenter',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='recording_same_experimenter',
        ),
        migrations.AddField(
            model_name='intervention',
            name='amount_per_week',
            field=models.PositiveIntegerField(default=1, verbose_name='Hoe vaak per week vindt de interventiesessie plaats?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='intervention',
            name='period',
            field=models.TextField(default=1, verbose_name='Wat is de periode waarbinnen de interventie plaatsvindt?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='intervention',
            name='post_duration',
            field=models.PositiveIntegerField(null=True, verbose_name='Wat is de duur van de nameting (in minuten)?', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='post_registration_kinds',
            field=models.ManyToManyField(related_name='post_registration_kinds', verbose_name='Kies het soort meting', to='core.RegistrationKind', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='post_registration_kinds_details',
            field=models.CharField(max_length=200, verbose_name='Namelijk', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='post_registrations',
            field=models.ManyToManyField(related_name='post_registrations', verbose_name='Hoe worden de gegevens bij de nameting vastgelegd?', to='core.Registration'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='post_registrations_details',
            field=models.CharField(max_length=200, verbose_name='Namelijk', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='pre_duration',
            field=models.PositiveIntegerField(null=True, verbose_name='Wat is de duur van de voormeting (in minuten)?', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='pre_registration_kinds',
            field=models.ManyToManyField(related_name='pre_registration_kinds', verbose_name='Kies het soort meting', to='core.RegistrationKind', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='pre_registration_kinds_details',
            field=models.CharField(max_length=200, verbose_name='Namelijk', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='pre_registrations',
            field=models.ManyToManyField(related_name='pre_registrations', verbose_name='Hoe worden de gegevens bij de voormeting vastgelegd?', to='core.Registration'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='pre_registrations_details',
            field=models.CharField(max_length=200, verbose_name='Namelijk', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='prepost_description',
            field=models.TextField(verbose_name='Geef een precieze beschrijving van de voor- en nameting', blank=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='prepost_experimenter',
            field=models.ForeignKey(verbose_name='Wie voert de voor- en nameting uit?', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='duration',
            field=models.PositiveIntegerField(verbose_name='Wat is de duur van de interventie per sessie in minuten?'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='experimenter',
            field=models.TextField(verbose_name='Wie voert de interventie uit?'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-06 13:52
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_session_leader_has_coc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='setting',
            field=models.ManyToManyField(blank=True, to='core.Setting', verbose_name='Geef aan waar de dataverzameling plaatsvindt'),
        ),
        migrations.AlterField(
            model_name='session',
            name='tasks_duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='De totale geschatte netto taakduur van uw sessie komt op basis van uw opgave per taak uit op <strong>%d minuten</strong>. Hoe lang duurt <em>de totale sessie</em>, inclusief ontvangst, instructies per taak, pauzes tussen taken, en debriefing? (bij labbezoek dus van binnenkomst tot vertrek)'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschrijf de taak die de deelnemer moet uitvoeren, en leg kort uit hoe deze taak (en de eventuele manipulaties daarbinnen) aan de beantwoording van uw onderzoeksvragen bijdraagt. Geef, kort, een paar voorbeelden (of beschrijvingen) van het type stimuli dat u van plan bent aan de deelnemer aan te bieden. Het moet voor de commissieleden duidelijk zijn wat u precies gaat doen.'),
        ),
        migrations.AlterField(
            model_name='task',
            name='duration',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Wat is de duur van deze taak van begin tot eind in <strong>minuten</strong>, dus vanaf het moment dat de taak van start gaat tot en met het einde van de taak (exclusief instructie maar inclusief oefensessie)? Indien de taakduur per deelnemer varieert (self-paced taak of task-to-criterion), geef dan <strong>het redelijkerwijs te verwachten maximum op</strong>.'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Wat is de naam van de taak?'),
        ),
    ]

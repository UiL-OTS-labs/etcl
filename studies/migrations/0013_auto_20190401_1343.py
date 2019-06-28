# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-01 11:43
from __future__ import unicode_literals

import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0012_auto_20180914_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='director_consent_declaration',
            field=models.FileField(blank=True, help_text='If it is already signed, upload the signed declaration form. If it is not signed yet, you can upload the unsigned document and send the document when it is signed to the secretary of the FEtC-H', upload_to='', validators=[core.validators.validate_pdf_or_doc], verbose_name='Upload hier de toestemmingsverklaring van de schoolleider/hoofd van het departement (in .pdf of .doc(x)-format)'),
        ),
        migrations.AlterField(
            model_name='study',
            name='compensation',
            field=models.ForeignKey(blank=True, help_text='Het standaardbedrag voor vergoeding aan de deelnemers is €10,- per uur. Minderjarigen mogen geen geld ontvangen, maar wel een cadeautje.', null=True, on_delete=django.db.models.deletion.CASCADE, to='studies.Compensation', verbose_name='Welke vergoeding krijgt de deelnemer voor zijn/haar deelname?'),
        ),
        migrations.AlterField(
            model_name='study',
            name='has_sessions',
            field=models.BooleanField(default=False, verbose_name='Taakonderzoek en interviews'),
        ),
        migrations.AlterField(
            model_name='study',
            name='passive_consent',
            field=models.NullBooleanField(help_text='Wanneer u kinderen via een instelling (dus ook school) werft en u de ouders niet laat ondertekenen, maar in plaats daarvan de leiding van die instelling, dan maakt u gebruik van passieve informed consent. U kunt de templates vinden op <a href="https://fetc-gw.wp.hum.uu.nl/toestemmingsverklaringen/" target="_blank">de FETC-GW-website</a>.', verbose_name='Maakt u gebruik van passieve informed consent?'),
        ),
    ]

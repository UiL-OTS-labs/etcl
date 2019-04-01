# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-01 11:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('proposals', '0018_auto_20190124_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(unique=True)),
                ('description', models.CharField(max_length=200)),
                ('reviewing_chamber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
            ],
        ),
        migrations.AlterField(
            model_name='proposal',
            name='is_pre_approved',
            field=models.NullBooleanField(default=None, verbose_name='Heeft u formele toestemming van een ethische toetsingcommissie, uitgezonderd deze FETC-GW commissie?'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='other_applicants',
            field=models.BooleanField(default=False, verbose_name='Zijn er nog andere onderzoekers bij deze studie betrokken die geaffilieerd zijn aan één van de onderzoeksinstituten ICON, OFR, OGK of UiL OTS?'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='other_stakeholders',
            field=models.BooleanField(default=False, verbose_name='Zijn er nog andere onderzoekers bij deze studie betrokken die <strong>niet</strong> geaffilieerd zijn aan een van de onderzoeksinstituten van de Faculteit Geestwetenschappen van de UU? '),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='relation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposals.Relation', verbose_name='In welke hoedanigheid bent u betrokken bij deze studie?'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Concept'), (40, 'Opgestuurd ter beoordeling door eindverantwoordelijke'), (50, 'Opgestuurd ter beoordeling door FETC-GW'), (55, 'Studie is beoordeeld door FETC-GW'), (60, 'Studie is beoordeeld door FETC-GW')], default=1),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='supervisor',
            field=models.ForeignKey(blank=True, help_text='Aan het einde van de procedure kunt u deze studie ter verificatie naar uw eindverantwoordelijke sturen. De eindverantwoordelijke zal de studie vervolgens kunnen aanpassen en indienen bij de FETC-GW.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Eindverantwoordelijke onderzoeker'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='title',
            field=models.CharField(help_text='De titel die u hier opgeeft is zichtbaar voor de FETC-GW-leden en, wanneer de studie is goedgekeurd, ook voor alle medewerkers die in het archief van deze portal kijken. De titel mag niet identiek zijn aan een vorige titel van een studie die u heeft ingediend.', max_length=200, unique=True, verbose_name='Wat is de titel van uw studie? Deze titel zal worden gebruikt in alle formele correspondentie.'),
        ),
        migrations.AlterField(
            model_name='wmo',
            name='metc',
            field=models.CharField(blank=True, choices=[('Y', 'ja'), ('N', 'nee'), ('?', 'twijfel')], default=None, max_length=1, verbose_name='Vindt de dataverzameling plaats binnen het UMC Utrecht of andere instelling waar toetsing door een METC verplicht is gesteld?'),
        ),
        migrations.AlterField(
            model_name='wmo',
            name='metc_application',
            field=models.BooleanField(default=False, verbose_name='Uw studie moet beoordeeld worden door de METC, maar dient nog wel bij de FETC-GW te worden geregistreerd. Is deze studie al aangemeld bij een METC?'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='institution',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='proposals.Institution', verbose_name='Aan welk onderzoeksinstituut bent u verbonden?'),
            preserve_default=False,
        ),
    ]

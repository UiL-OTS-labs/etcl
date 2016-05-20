# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0017_auto_20160520_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='passive_consent',
            field=models.BooleanField(default=False, help_text='Wanneer u kinderen via een instelling (dus ook school) werft en u de ouders niet laat ondertekenen, maar in plaats daarvan de leiding van die instelling, dan maakt u gebruik van passieve informed consent. U kunt de templates vinden op <a href="https://etcl.wp.hum.uu.nl/toestemmingsverklaringen/" target="_blank">de ETCL-website</a>.', verbose_name='Maakt u gebruik van passieve informed consent?'),
        ),
    ]

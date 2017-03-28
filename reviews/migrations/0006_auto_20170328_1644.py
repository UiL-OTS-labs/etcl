# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_review_date_should_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='confirmation_comments',
            field=models.TextField(verbose_name='Ruimte voor eventuele opmerkingen', blank=True),
        ),
        migrations.AddField(
            model_name='review',
            name='confirmation_sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

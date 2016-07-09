# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primer_design', '0002_auto_20160317_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='primer',
            name='maxnumber',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='primer',
            name='rangelength',
            field=models.IntegerField(default=100, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primer_design', '0003_auto_20160321_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primer',
            name='rangelength',
            field=models.IntegerField(default=1000, blank=True),
        ),
    ]

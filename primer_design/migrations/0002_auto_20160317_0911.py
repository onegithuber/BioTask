# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primer_design', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='primer',
            name='id',
        ),
        migrations.AlterField(
            model_name='primer',
            name='name',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='primer',
            name='sequen',
            field=models.FileField(upload_to=b'media/hla'),
        ),
    ]

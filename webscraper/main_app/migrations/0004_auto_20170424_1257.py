# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20170421_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]

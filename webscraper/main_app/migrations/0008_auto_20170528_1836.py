# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-28 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20170517_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourceprofile',
            name='profileNumber',
        ),
        migrations.AddField(
            model_name='sourceprofile',
            name='profileName',
            field=models.CharField(default='', max_length=150),
        ),
    ]

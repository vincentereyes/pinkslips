# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-03 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinkslips', '0011_auto_20180303_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='latitude2',
            field=models.FloatField(default=-121.9123471),
        ),
        migrations.AddField(
            model_name='conversation',
            name='longitude2',
            field=models.FloatField(default=37.3753997),
        ),
    ]

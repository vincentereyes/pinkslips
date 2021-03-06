# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-02 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinkslips', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='latitude',
            field=models.FloatField(default=-121.91015303558203),
        ),
        migrations.AddField(
            model_name='conversation',
            name='longitude',
            field=models.FloatField(default=37.37541248891094),
        ),
        migrations.AlterField(
            model_name='image',
            name='content',
            field=models.FileField(upload_to=b''),
        ),
    ]

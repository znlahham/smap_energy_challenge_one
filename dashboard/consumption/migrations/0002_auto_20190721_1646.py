# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-21 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumption', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='user_consump_avg',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='userdata',
            name='user_consump_total',
            field=models.FloatField(default=0),
        ),
    ]

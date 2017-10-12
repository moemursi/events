# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_auto_20171001_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportsgroup',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='date_issued',
            field=models.DateField(auto_now_add=True),
        ),
    ]
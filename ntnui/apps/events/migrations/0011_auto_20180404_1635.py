# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-04 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_subeventdescription_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subeventdescription',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='description'),
        ),
    ]
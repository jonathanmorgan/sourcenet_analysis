# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_analysis', '0003_auto_20160303_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='reliability_names_results',
            name='author_lookup_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reliability_names_results',
            name='subject_lookup_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 01:16
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('context_analysis', '0013_auto_20160817_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='reliability_names',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
